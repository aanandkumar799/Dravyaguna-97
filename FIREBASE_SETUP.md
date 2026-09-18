# Firebase / GitHub production setup

The DravyaGuna 97 site uses Firebase project **dravya-guna-97** for authenticated feedback and Firestore storage. GitHub Pages remains the primary public site.

## 1. Firebase web configuration

The public web configuration is stored in `feedback-config.js`. Firebase web API keys are not database credentials; Firestore and Authentication rules provide the access control.

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

## 5. Production deployment

The single Firebase deployment workflow is:

`.github/workflows/firebase-deploy.yml`

It deploys:

1. Firestore security rules
2. Firebase Hosting

The workflow verifies that the service-account JSON belongs to project `dravya-guna-97` and fails if Firestore rules deployment fails.

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
