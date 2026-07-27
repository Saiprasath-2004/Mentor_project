Remember this forever.

ForeignKey	                relationship
Database concept	        SQLAlchemy ORM concept
Maintains data integrity	Connects Python objects
Creates DB constraint	    Enables object naviga

Things to see before creating a Team Member table  and writing service layer

1. Does the team exist?

↓

2. Does current user own this team?

↓

3. Does target user exist?

↓

4. Is target user already a member?

↓

5. Create membership

↓

6. Return response