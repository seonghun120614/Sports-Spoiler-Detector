"""
Abstract Database Access
Want to switch from PostgreSQL to MongoDB in the future? Or mock the DB in tests?

Repositories make that possible.

They abstract away the ORM/database and expose clean methods like:

```
def get_user_by_email(email: str) -> User: ...
```

Ref: https://medium.com/the-pythonworld/the-architecture-blueprint-every-python-backend-project-needs-207216931123
"""