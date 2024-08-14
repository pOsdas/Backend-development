import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


# table of contents
# create
async def create_user(session: AsyncSession, user_name: str) -> User:
    user = User(user_name=user_name)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def create_user_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def create_posts(
        session: AsyncSession,
        user_id: int,
        *posts_titles: str,
) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    print("posts", posts)
    return posts


# get
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.user_name == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def get_users_with_posts(
        session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    result: Result = await session.execute(stmt)
    users = result.scalars()

    # for user in users:  # type: User
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("post", post)
        print("author", post.user)


# posts and profiles
async def get_users_with_posts_and_profiles(
        session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        # .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        # .where(User.user_name == "john")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


# show
async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        # print(user.profile.first_name)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, user_name="alice")
        # # await create_user(session=session, user_name="john")
        # # await create_user(session=session, user_name="sam")
        # user_john = await get_user_by_username(session, username="john")
        # user_sam = await get_user_by_username(session, username="sam")
        # user_alice = await get_user_by_username(session, username="alice")
        # # user_bob = await get_user_by_username(session, username="bob")
        #
        # await create_user_profile(
        #     session=session,
        #     user_id=user_john.id,
        #     first_name="John",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_alice.id,
        #     first_name="Alice",
        #     last_name="Selezneva"
        # )
        # await show_users_with_profiles(session=session)
        # await create_posts(
        #     session,
        #     user_john.id,
        #     "SQLA 2.0",
        #     "SQLA Joins",
        # )
        #
        # await create_posts(
        #     session,
        #     user_sam.id,
        #     "FastAPI intro",
        #     "FastAPI Advanced",
        #     "FastAPI more",
        # )
        # await get_users_with_posts(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == '__main__':
    asyncio.run(main())
