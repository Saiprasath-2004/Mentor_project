from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_models import Team

class TeamRepository:

    #persist a new team in the database
    async def create_team(self, db: AsyncSession, team_data: dict) -> Team:
        
        team = Team(**team_data)

        db.add(team)
        await db.commit()

        await db.refresh(team)

        return team


    #Return all the teams owned by a specific user
    async def get_user_teams(self, db: AsyncSession, owner_id) -> list[Team]:

        query = (select(Team).where(Team.owner_id == owner_id))
        result = await db.execute(query)
        return result.scalars().all()


    #return the team by id
    async def get_team_by_id(self,db: AsyncSession, team_id) -> Team | None:
        query =  (select(Team).where(Team.id == team_id))
        result = await db.execute(query)
        return  result.scalar_one_or_none()
    
    # Persist updated team details
    async def update_team(self,db: AsyncSession, team: Team) -> Team:
        await db.commit()
        await db.refresh(team)

        return team
    
    # Permanently remove a team from the database
    async def delete_team(self,db: AsyncSession, team: Team):
        await db.delete(team)
        await db.commit()
    
