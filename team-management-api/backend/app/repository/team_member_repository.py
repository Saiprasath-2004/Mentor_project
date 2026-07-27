from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_member_models import TeamMember
from app.schemas.team_member_schemas import TeamMemberCreate

class TeamMemberRepository:
    #Create a new team membership
    async def create_member(
        self,
        db: AsyncSession,
        team_id: UUID,
        member_data: TeamMemberCreate
    ) -> TeamMember:
        
        member = TeamMember(
            team_id = team_id,
            user_id = member_data.user_id,
            role=member_data.role
        )

        db.add(member)
        await db.commit()
        await db.refresh(member)

        return member
    

    #Return a specific member of a team 
    async def get_member(
        self,
        db: AsyncSession,
        team_id: UUID,
        user_id: UUID
    )  -> TeamMember | None:
        query = ( select(TeamMember).where(TeamMember.team_id == team_id,
                                           TeamMember.user_id == user_id))
        
        result = await db.execute(query)
        return result.scalar_one_or_none()



    # Return all members of a team
    async def list_members(
        self,
        db: AsyncSession,
        team_id: UUID
    ) -> list[TeamMember]:
        
        query = (select(TeamMember).where(TeamMember.team_id == team_id))

        result = await db.execute(query)
        return result.scalars().all()


    #Delete the member from a team
    async def remove_member(
            self,
            db:AsyncSession,
            member: TeamMember
    ):
        
        await db.delete(member)

        await db.commit()
        