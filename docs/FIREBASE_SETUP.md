# Firebase / GitHub production setup

The DravyaGuna 97 site uses Firebase project **dravya-guna-97** for authenticated feedback and Firestore storage. GitHub Pages remains the primary public site.

## 1. Firebase web configuration

The public web configuration is stored in `feedback-config.js`. Firebase web API keys are not database credentials; Firestore and Authentication rules provide the access control. The feedback and administrator pages use browser-session Firebase persistence, so closing the browser ends the local sign-in session. Never replace this public configuration with a service-account key; service-account credentials belong only in the GitHub `firebase-production` environment secret.

## 2. Authentication

In Firebase Console:

- Project: `dravya-guna-97`
- Authentication → Sign-in method → **Google** enabled
- Authentication → Settings → Authorized domains must include:
  - `aanandkumar799.github.io`
  - the Firebase Hosting domain if Firebase Hosting is used

## 3. Firestore

Create/enable Firestore Database for the project.

The production rules are in `firestore.rules`:

- only verified Google accounts can create feedback
- the authenticated UID/email must match the submitted user identity
- users cannot read, update, or delete reviews
- the configured admin email can read/update/delete reviews

## 4. GitHub Actions credential

The repository uses the GitHub environment **`firebase-production`**.

Create this environment secret:

`FIREBASE_SERVICE_ACCOUNT_DRAVYA_GUNA_97`

The value must be the complete Firebase service-account JSON generated from:

**Firebase Console → Project settings → Service accounts → Firebase Admin SDK → Generate new private key**

Never commit this JSON to the repository or paste it into an issue/chat.

The CI service account must also have these Google Cloud IAM permissions on `dravya-guna-97`:

- `roles/firebasehosting.admin` (or an equivalent Hosting deployment role)
- `roles/serviceusage.serviceUsageConsumer`

The second role is required for the Firebase CLI to query the `firebasehosting.googleapis.com` service. Without it, the Hosting workflow fails with HTTP 403 before deployment begins. A Firebase/Google Cloud administrator can grant it with:

```bash
gcloud projects add-iam-policy-binding dravya-guna-97 \
  --member="serviceAccount:CI_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/serviceusage.serviceUsageConsumer"
```

Replace `CI_SERVICE_ACCOUNT_EMAIL` with the `client_email` from the GitHub environment secret.

## 5. Production deployment

The single Firebase deployment workflow is:

`.github/workflows/firebase-deploy.yml`

It deploys:

1. Firebase Hosting
2. Firestore security rules

The Hosting workflow verifies that the service-account JSON belongs to project `dravya-guna-97`. Firestore rules are deployed by the separate `.github/workflows/firebase-rules.yml` workflow.

Duplicate Firebase deployment workflows were removed to prevent conflicting deployments.

## 6. GitHub Pages

`.github/workflows/deploy.yml` deploys the public GitHub Pages site and performs database/artifact validation before publishing.

## 7. Feedback test

After a successful Firebase deployment:

1. Open `https://aanandkumar799.github.io/Dravyaguna-97/feedback.html`
2. Sign in with a verified Google account.
3. Submit a short test message with a 1–5 rating.
4. Confirm the success message.
5. The admin dashboard is `admin-feedback.html` and is restricted by the Firestore rules to the configured admin email.

If submission still returns `permission-denied`, verify the deployed Firestore rules and the Firebase Authentication Google provider/authorized domain settings in the Firebase Console.
