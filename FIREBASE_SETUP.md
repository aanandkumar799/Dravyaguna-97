# Firebase feedback setup

The feedback form is wired by `firebase-feedback.js` to Cloud Firestore collection `reviews`.

## Required Firebase Console step

In Firebase Console for `dravya-guna-97`:

1. Build → Firestore Database → Create database.
2. Create the database in your chosen region.
3. Add/verify the web app under Project settings → Your apps.
4. Deploy Firestore Security Rules that allow the intended feedback submission pattern.

Example starting rule (tighten further before production if you add authentication/admin tooling):

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /reviews/{reviewId} {
      allow create: if request.resource.data.name is string
        && request.resource.data.review is string
        && request.resource.data.name.size() >= 1
        && request.resource.data.name.size() <= 100
        && request.resource.data.review.size() >= 1
        && request.resource.data.review.size() <= 5000;
      allow read, update, delete: if false;
    }
  }
}
```

`firebase-feedback.js` uses the Firebase Web SDK directly from Google's CDN and writes feedback to Firestore. The Firebase web configuration is not a server credential; do not put Firebase Admin/service-account private keys in this repository.
