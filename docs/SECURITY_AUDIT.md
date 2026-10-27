# Security checklist assessment

Audit date: 2026-10-23  
Repository: `aanandkumar799/Dravyaguna-97`  
Scope: repository contents, Git history, Firebase configuration/rules, GitHub Actions, and the existing validation scripts.

## Executive summary

The project is primarily a static HTML/CSS/JavaScript learning site. Its only authenticated backend feature is Google-authenticated feedback stored in Firebase Firestore. There is no custom server, password database, SQL database, file-upload endpoint, webhook receiver, or server-side URL fetcher in the repository.

Concrete changes made during this audit:

- Added Firebase Hosting security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, and a baseline CSP.
- Changed feedback and administrator Firebase sessions from persistent `LOCAL` persistence to browser-session `SESSION` persistence.
- Removed verbose Firebase error logging from the feedback and administrator pages; user-facing messages remain generic while preserving useful error codes where needed.
- Confirmed Firestore rules enforce verified Google authentication, identity binding, field allow-lists, input bounds, and administrator-only reads/updates/deletes.
- Confirmed repository validation scripts pass and no private-key, cloud-secret, password, or token credential was found.

The Firebase web `apiKey` in `feedback-config.js` is a public client identifier, not a database credential. It is expected to be shipped to browsers for Firebase web SDK initialization. It must still be protected by Firebase Authentication and Firestore rules; those rules are the real access control. It was found in Git history as well, but it is not a secret requiring rotation unless Firebase Console restrictions or abuse monitoring indicate compromise.

## Control-by-control result

Legend: **Addressed** = checked and fixed/verified in the repository. **Applicable—external check** = repository cannot prove the production setting. **Not applicable** = no matching feature exists. **Partial** = meaningful repository controls exist but additional production or architectural work is required.

### 1. Secrets and environment security

| # | Result | Assessment |
|---|---|---|
| 1 | Partial | No private secrets are in frontend code. The Firebase web API key is intentionally public client configuration, not a credential. |
| 2 | Applicable—external check | Firebase/GitHub production settings must be checked in their consoles. Repository deployment validation is present. |
| 3 | Not applicable | There is no AI Gateway or server-side API secret in this project. |
| 4 | Not applicable | The application does not mint or verify its own JWTs; Firebase manages tokens. |
| 5 | Addressed | Current tree and Git history were searched for common private-key, cloud-key, password, and token patterns. No private credential was found. |
| 6 | Not required | No confirmed exposed credential was found. Do not rotate the public Firebase web identifier solely because it is visible. |
| 7 | Addressed | No default password or credential was found. Firebase service-account JSON is referenced only through a GitHub environment secret. |
| 8 | Addressed | Verbose Firebase console logging was removed from feedback/admin pages; user-facing errors are generic. |

### 2. Authentication and authorization

| # | Result | Assessment |
|---|---|---|
| 9 | Addressed | Feedback creation requires a verified Google-authenticated Firebase user in Firestore rules. |
| 10 | Addressed | The admin page has a Google sign-in gate, and Firestore read/update/delete access is independently restricted by rules to the configured administrator email. |
| 11 | Addressed | Authorization is enforced server-side by Firestore rules, not only by client UI checks. |
| 12 | Partial | Runtime Firestore access is narrow. The Firebase service account used by CI should continue to have only the minimum Hosting/rules deployment roles required. |
| 13 | Addressed | No object-level data endpoint exists; reviews are not readable by ordinary users, and admin access is rule-gated. |
| 14 | Addressed | Review creation binds submitted UID/email to `request.auth`; users cannot read other users' reviews. |
| 15 | Applicable—external check | Google sign-in is enabled and is stronger than a local password flow. MFA for the administrator Google account should be verified in Google Workspace/Google Account settings. |
| 16 | Not applicable | The project does not store or process passwords. |
| 17 | Addressed | Firebase persistence was changed from `LOCAL` to `SESSION` for feedback and admin pages, avoiding long-lived browser sessions where possible. |

### 3. API and request security

| # | Result | Assessment |
|---|---|---|
| 18 | Not applicable | No SQL or server-side query construction exists. Firestore SDK calls and rules are used instead. |
| 19 | Addressed | Dynamic HTML output is escaped in the reviewed rendering paths, including feedback/admin data and plant records. Existing syntax checks pass. |
| 20 | Addressed | Feedback input is bounded and validated in both the client and Firestore rules; generated content is escaped before insertion. |
| 21 | Not applicable | The app does not expose cookie-authenticated custom POST endpoints. Firebase SDK requests use Firebase authentication and Firestore rules. |
| 22 | Partial | Feedback requires verified Google authentication, which provides baseline abuse resistance. A strict per-user rate limit would require a trusted backend or additional Firestore design and is not safely implementable in client-only code. |
| 23 | Addressed | Firestore rules authorize every read/write operation; admin UI checks are not the sole protection. |
| 24 | Applicable—external check | Firebase Authentication authorized domains and any Firebase/GitHub hosting origin settings must be kept explicit and limited to the intended domains. |
| 25 | Not applicable | No file upload feature or upload endpoint exists. |
| 26 | Not applicable | No webhook receiver exists. |
| 27 | Not applicable | No server-side request feature exists; browser requests are to fixed application/data hosts and configured Firebase services. |
| 28 | Addressed | Firestore rules constrain field names, types, enum values, string lengths, and rating ranges. |

### 4. Database and data protection

| # | Result | Assessment |
|---|---|---|
| 29 | Applicable—external check | Database/service-account permissions are managed in Firebase/GitHub. The workflow verifies the service-account project ID and removes the temporary JSON file. |
| 30 | Addressed | Firestore rules provide the applicable document-level equivalent of row-level access control. |
| 31 | Not applicable | No SQL queries or unsafe query strings exist. |
| 32 | Addressed | Review documents are readable only by the administrator; user identity fields are allow-listed and bound to authenticated claims. |
| 33 | Applicable—external check | Firebase backup/restore and retention must be confirmed in the Firebase project. Repository data is also versioned in Git, but that is not a Firestore backup substitute. |
| 34 | Addressed | Existing generation and pre-deploy validation scripts verify the 97 canonical records, generated artifacts, and sitemap. Existing content is not intentionally deleted by the security changes. |

### 5. Application and deployment security

| # | Result | Assessment |
|---|---|---|
| 35 | Addressed—Firebase Hosting | Added security headers and a baseline CSP to `firebase.json`. GitHub Pages does not honor Firebase response headers, so equivalent headers require GitHub Pages/CDN configuration if GitHub Pages remains the primary public host. |
| 36 | Addressed | No production debug mode was found; verbose client error logging was removed from the authenticated pages. |
| 37 | Applicable—external check | There is no application package manifest or runtime dependency lockfile. Firebase SDK scripts are pinned to explicit versions; these hosted versions should be reviewed periodically. |
| 38 | Not applicable | No package-manager lockfile is present because the site has no package-managed runtime. |
| 39 | Partial | No obvious test endpoint or unused server package was found. Static legacy/generated files remain by design and are covered by existing site checks. |
| 40 | Addressed | Tracked files were checked for backups, private config, credentials, and source maps. No sensitive artifact was found. |
| 41 | Applicable—external check | Verify Firebase Hosting, GitHub Pages, repository environment, and branch-protection/deployment permissions in their respective consoles. |
| 42 | Addressed | No `.env`, private key, service-account JSON, or private configuration file is tracked. The deployment secret is referenced through GitHub environment secrets. |
| 43 | Partial | Workflows use explicit permissions. Deployment workflows have only the permissions needed for their deployment target; autonomous image/site workflows require `contents: write` because they commit generated assets. Review whether those autonomous commits are acceptable for the branch policy. |

### 6. Testing and final verification

| # | Result | Assessment |
|---|---|---|
| 44 | Addressed—repository scope | Repository inspection, history scan, Firebase rule review, workflow review, and existing static checks were completed. A live infrastructure audit still requires access to the deployed services. |
| 45 | Addressed—rules scope | Firestore rules enforce verified identity and administrator-only reads; cross-user review isolation is explicit. Live authenticated tests remain recommended after deployment. |
| 46 | Addressed—repository scope | CodeQL workflow is enabled for JavaScript and Python; existing validation and JavaScript syntax checks pass. No package dependency audit applies because no package manifest exists. |
| 47 | Addressed | Authenticated pages now avoid verbose console error output and show generic user-facing messages. Rendered user data is escaped. |
| 48 | Addressed | Existing `predeploy-validation.py`, `public-readiness.py`, `check-site.py`, and `check-inline-js.py` all pass after the changes. |
| 49 | Applicable—external check | After deployment, verify response headers, Google sign-in, feedback submission, admin isolation, and both public hosting origins if both remain active. |
| 50 | Addressed—repository scope | The security edits are limited to headers, session persistence, and error handling. Existing content-generation and site validation checks pass, including 97 canonical records and 108 sitemap URLs. |

## Remaining production checks

1. Verify Firebase Authentication authorized domains contain only the intended production domains.
2. Confirm the administrator Google account has MFA enabled.
3. Confirm the GitHub `firebase-production` environment secret is present, scoped to the environment, and backed by a least-privilege service account.
4. Confirm Firebase Firestore backups/retention are configured if feedback data must be recoverable independently of Git.
5. If GitHub Pages is the primary public origin, configure security headers at the GitHub Pages/CDN layer or put the site behind a header-capable reverse proxy; `firebase.json` headers apply only to Firebase Hosting.
6. Run an authenticated smoke test after the next deployment: ordinary verified user can create feedback but cannot read it, while the administrator can read it.
