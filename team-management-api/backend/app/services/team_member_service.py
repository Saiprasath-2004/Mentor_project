from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.team_member_repository import TeamMemberRepository
from app.repository.team_repository import TeamRepository
from app.repository.user_repository import UserRepository
from app.schemas.team_member_schemas import (
    TeamMemberCreate,
    TeamMemberResponse,
)
from app.services.activity_service import ActivityService
from app.core.enums import ActivityAction



class TeamMemberService:

    def __init__(self):
        self.team_repo = TeamRepository()
        self.user_repo = UserRepository()
        self.member_repo = TeamMemberRepository()
        self.activity_service = ActivityService()

    # Add a user into a team
    async def add_member(
        self,
        db: AsyncSession,
        team_id: UUID,
        member_data: TeamMemberCreate,
        current_user: User
    ) -> TeamMemberResponse:

        # Check team exists
        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        # Only owner can invite members
        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the team owner can add members."
            )

        # Check invited user exists
        user = await self.user_repo.get_by_id(
            db,
            member_data.user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # Prevent duplicate membership
        existing_member = await self.member_repo.get_member(
            db,
            team_id,
            member_data.user_id
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member."
            )

        # Save membership
        member = await self.member_repo.create_member(
            db,
            team_id,
            member_data
        )

        await self.activity_service.create_activity(
            db=db,
            team_id=team.id,
            user_id=current_user.id,
            action=ActivityAction.MEMBER_ADDED,
            description=f'Added a new member to "{team.name}"'
        )

        return TeamMemberResponse.model_validate(member)

    # Return every member inside a team
    async def list_members(
        self,
        db: AsyncSession,
        team_id: UUID,
        current_user: User
    ) -> list[TeamMemberResponse]:

        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found."
            )

        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view members."
            )

        members = await self.member_repo.list_members(
            db,
            team_id
        )

        return [
            TeamMemberResponse.model_validate(member)
            for member in members
        ]

    # Remove a member from the team
    async def remove_member(
        self,
        db: AsyncSession,
        team_id: UUID,
        user_id: UUID,
        current_user: User
    ):

        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found."
            )

        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only owner can remove members."
            )

        member = await self.member_repo.get_member(
            db,
            team_id,
            user_id
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found."
            )

        await self.activity_service.create_activity(
            db=db,
            team_id=team.id,
            user_id=current_user.id,
            action=ActivityAction.MEMBER_REMOVED,
            description=f'Removed a member from "{team.name}"'
        )

        await self.member_repo.remove_member(
            db,
            member
        )