# Project Setting
export PROJECT_ID=learn-terraform-311311

# Project Region
export REGION=europe-west2

# Project Service
export SERVICE_NAME=alumni

# Service Accounts
export CLOUDRUN_SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# Database Settings
export INSTANCE_NAME=alumni-sql
export ROOT_PASSWORD=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
export DATABASE_INSTANCE=$PROJECT_ID:$REGION:$INSTANCE_NAME

export DBUSERNAME=alumni-django
export DBPASSWORD=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 40 | head -n 1)
export DATABASE_NAME=alumni
export DATABASE_URL=postgres://$DBUSERNAME:${DBPASSWORD}@//cloudsql/$PROJECT_ID:$REGION:$INSTANCE_NAME/$DATABASE_NAME

# Storage Settings
export GS_BUCKET_NAME=${PROJECT_ID}-$DATABASE_NAME-media


# GLOUD Configuration
gcloud config set run/platform managed
gcloud config set run/region $REGION


# ENABLE APIs
gcloud services enable \
  run.googleapis.com \
  iam.googleapis.com \
  compute.googleapis.com \
  sql-component.googleapis.com \
  sqladmin.googleapis.com \
  cloudbuild.googleapis.com \
  cloudkms.googleapis.com \
  cloudresourcemanager.googleapis.com \
  secretmanager.googleapis.com

# CREATE CLOUD RUN SERVICE WITH CLOUDRUN SERVICE ACCOUNT
gcloud iam service-accounts create $SERVICE_NAME --display-name "$SERVICE_NAME service account"

# CREATE CLOUDRUN SERVICE ACCOUNT
for role in cloudsql.client run.admin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$CLOUDRUN_SA \
    --role roles/${role}
done

# CREATE CLOUD SQL INSTANCE
gcloud sql instances create $INSTANCE_NAME \
  --database-version POSTGRES_12 \
  --tier db-f1-micro  \
  --region $REGION \
  --project $PROJECT_ID \
  --root-password $ROOT_PASSWORD

# CREATE CLOUD SQL DATABASE
gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# CREATE CLOUD SQL DATABASE USER
gcloud sql users create $DBUSERNAME --password $DBPASSWORD --instance $INSTANCE_NAME


# gcloud sql connect $INSTANCE_NAME
# CREATE USER "<DBUSERNAME>" WITH PASSWORD "<DBPASSWORD>"; 
# GRANT ALL PRIVILEGES ON DATABASE "<DATABASE_NAME>" TO "<DBUSERNAME>";


# CREATE CLOUD STORAGE
gsutil mb -l ${REGION} gs://${GS_BUCKET_NAME}
gsutil iam ch serviceAccount:${CLOUDRUN_SA}:roles/storage.objectAdmin gs://${GS_BUCKET_NAME}

# GET and SET PROJECTNUM
export PROJECTNUM=$(gcloud projects describe ${PROJECT_ID} --format 'value(projectNumber)')

# SET CLOUDBUILD SERVICE ACCOUNT
export CLOUDBUILD_SA=${PROJECTNUM}@cloudbuild.gserviceaccount.com

# CREATE .ENV FILE
echo DATABASE_URL=\"${DATABASE_URL}\" > .env
echo GS_BUCKET_NAME=\"${GS_BUCKET_NAME}\" >> .env
echo SECRET_KEY=\"$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)\" >> .env


# CREATE SECRETS
gcloud secrets create django_alumni_settings --replication-policy automatic --data-file .env

# ALLOW ACCESS TO SECRETS FOR CLOUDRUN AND CLOUDBUID SERVICE ACCOUNT
gcloud secrets add-iam-policy-binding django_alumni_settings \
  --member serviceAccount:$CLOUDRUN_SA \
  --role roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding django_alumni_settings \
  --member serviceAccount:$CLOUDBUILD_SA \
  --role roles/secretmanager.secretAccessor

# SETTING SUPERUSER ACCOUNT SECRET
export SUPERUSER="admin"
gcloud secrets create SUPERUSER --replication-policy automatic
gcloud secrets add-iam-policy-binding SUPERUSER \
    --member serviceAccount:$CLOUDBUILD_SA \
    --role roles/secretmanager.secretAccessor

# SETTING SUPERUSER PASSWORD SECRET
export SUPERPASS=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 30 | head -n 1)
gcloud secrets create SUPERPASS --replication-policy automatic
gcloud secrets add-iam-policy-binding SUPERPASS \
    --member serviceAccount:$CLOUDBUILD_SA \
    --role roles/secretmanager.secretAccessor

# for SECRET in SUPERUSER SUPERPASS; do
#   echo -n "${SECRET}"
#   echo -n "${SECRET}"
#   echo $SECRET
# done

# for SECRET in SUPERUSER SUPERPASS; do
#   gcloud secrets create $SECRET --replication-policy automatic
#   echo -n "${!SECRET}" | gcloud secrets versions add $SECRET --data-file=-
#   gcloud secrets add-iam-policy-binding $SECRET \
#     --member serviceAccount:$CLOUDBUILD_SA \
#     --role roles/secretmanager.secretAccessor
# done

# ACCESS SECRETS
# gcloud secrets versions access latest --secret $SECRET

# BUILD CONTAINER
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

# DEPLOY CONTAINER
gcloud run deploy $SERVICE_NAME \
  --allow-unauthenticated \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
  --service-account $CLOUDRUN_SA

gcloud run services list

# UPDATE ENVIRONMENT VARIABLE FOR CURRENT_HOST URL
export SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --format "value(status.url)")
echo $SERVICE_URL
gcloud run services update $SERVICE_NAME --update-env-vars "CURRENT_HOST=${SERVICE_URL}"


# ADDING ROLES (SQLCLIENT AND ADMIN) TO CLOUDBUILD SERVICE ACCOUNT
for role in cloudsql.client run.admin; do
  gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member serviceAccount:${CLOUDBUILD_SA} \
    --role roles/${role}
done

# ADDING serviceAccountUser ROLE TO CLOUDBUILD SERVICE ACCOUNT
gcloud iam service-accounts add-iam-policy-binding ${CLOUDRUN_SA} \
  --member "serviceAccount:${CLOUDBUILD_SA}" \
  --role "roles/iam.serviceAccountUser"

# BUILD, MIGRATE AND DEPLOY
gcloud builds submit \
  --config .cloudbuild/build-migrate-deploy.yaml \
  --substitutions "_REGION=${REGION},_INSTANCE_NAME=${INSTANCE_NAME},_SERVICE=${SERVICE_NAME}"



# SETTING UP CONTINUOUS DEPLOYMENT TRIGGER VIA GITHUB REPO
REPO_OWNER=you
gcloud beta builds triggers create github \
  --repo-name django-demo-app-unicodex \
  --repo-owner ${REPO_OWNER} \
  --branch-pattern master \
  --build-config .cloudbuild/build-migrate-deploy.yaml \
  --substitutions "_REGION=${REGION},_INSTANCE_NAME=${INSTANCE_NAME},_SERVICE=${SERVICE_NAME}"

