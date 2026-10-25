# Guestbook

The portfolio’s Leave a note window opens a companion guestbook at https://tola-guestbook.axe-rhitta.chatgpt.site/.

Owner moderation: https://tola-guestbook.axe-rhitta.chatgpt.site/admin

Sign in with the owner’s ChatGPT account. Pending notes are private. Approve publishes a note. Hide removes it from the public wall; both decisions are reversible. Anonymous visitors cannot view pending notes or moderate.

Name and note are required; drawing a signature is optional. Visitors explicitly consent before submission. Notes are limited to 400 characters and submissions are rate-limited.

The service stores records in D1. ADMIN_EMAIL and RATE_SALT are secrets in the companion Site, never in this public repository. The initial moderator is bound to the authenticated site-scoped user ID.

Portfolio rollback: previous.html is the saved classic design. Copy it to index.html to revert the homepage without deleting guestbook data.
