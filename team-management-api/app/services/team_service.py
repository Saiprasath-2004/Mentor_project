from fastapi import HTTPException
from starlette import status

from app.repository.team_repository import TeamRepository
from app.schemas.team_schemas import TeamCreate, TeamResponse, TeamUpdate

class TeamService:

    def  __init__(self):
        self.team_repo = TeamRepository()

    # Fetch a team and ensure it belongs to the authenticated user
    async def _get_owned_team( self,  db, team_id, current_user):
        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this team"
            )
        return team

    #Create  a new team by the authenticated user 
    async def create_team(self, db, team_data: TeamCreate, current_user) -> TeamResponse:

        # convert validated schema into mutable dictionary
        team_dict = team_data.model_dump()

        # Backend decides ownership, never trust client input
        team_dict["owner_id"] = current_user.id

        # Persist team in database
        team = await self.team_repo.create_team(
            db,
            team_dict
        )

        # Return safe response schema
        return TeamResponse.model_validate(team)
    
    async def get_my_teams(self, db, current_user) -> list[TeamResponse]:
        teams = await self.team_repo.get_user_teams( db, current_user.id)

        return [
            TeamResponse.model_validate(team)
            for team in teams
        ]
 
    async def get_team(self, db, team_id, current_user) -> TeamResponse:
        team = await self._get_owned_team(
            db,
            team_id,
            current_user
        )
        
        return TeamResponse.model_validate(team)
    
    async def update_team(self, db, team_id,team_data: TeamUpdate,current_user) -> TeamResponse:

        #Reuse ownership validation
        team = await self._get_owned_team(
            db,
            team_id,
            current_user
        )
        
        #only update fields provided by clients
        updates = team_data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(team, field, value)

        updated_team = await self.team_repo.update_team(
            db,
            team
        )

        return TeamResponse.model_validate(updated_team)
    
    # Delete a team owned by the authenticated user
    async def delete_team(self,db, team_id,current_user):

        team = await self._get_owned_team(
            db,
            team_id,
            current_user
        )

        await self.team_repo.delete_team(
            db,
            team
        )