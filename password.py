"""
1. User clicks on forgot password link or in profile page user clicks on reset password.
2. User types their email in the text box field.
3. Check whether the email exists in the user table.
4. Create a table which has id, email, username, vcode, status 0, creation date.
6. Send an email to the user which contains "we have got a request for resetting your password". and has the vcode = ------. "Please click here to reset the password".
7. Email field vcode, new password, confirm password.
8. Verify if status = 1 or 0, accordingly if 1 : this page isn't accessible , if 0 : continue to next step.
9. Match the verification code with the one in the database and the one which the user enters.
10. Hatch the password and update into database.
"""