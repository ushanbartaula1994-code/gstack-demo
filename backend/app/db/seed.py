"""
Database seed data for AI Fitness Coach
"""

import asyncio
from datetime import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise import Exercise, DifficultyLevel, MuscleGroup
from app.models.user import User, UserProfile, FitnessLevel, FitnessGoal, EquipmentType


# Core exercises for MVP (5 exercises with form analysis)
CORE_EXERCISES_DATA = [
    {
        "name": "Squat",
        "description": "A fundamental lower body exercise targeting quadriceps, glutes, and hamstrings. Stand with feet shoulder-width apart, lower your hips until your thighs are parallel to the ground, then push back up.",
        "muscle_groups": MuscleGroup.QUADRICEPS,
        "secondary_muscles": "glutes,hamstrings,lower back",
        "difficulty": DifficultyLevel.BEGINNER,
        "equipment_required": "bodyweight",
        "category": "strength",
        "is_core_exercise": True,
        "form_analysis_available": True,
        "video_url": "/videos/squat.mp4",
        "image_url": "/images/squat.png",
    },
    {
        "name": "Push-up",
        "description": "A classic upper body exercise targeting chest, shoulders, and triceps. Start in a plank position, lower your chest to the ground, then push back up.",
        "muscle_groups": MuscleGroup.CHEST,
        "secondary_muscles": "shoulders,triceps,core",
        "difficulty": DifficultyLevel.BEGINNER,
        "equipment_required": "bodyweight",
        "category": "strength",
        "is_core_exercise": True,
        "form_analysis_available": True,
        "video_url": "/videos/pushup.mp4",
        "image_url": "/images/pushup.png",
    },
    {
        "name": "Lunge",
        "description": "A unilateral lower body exercise that works quadriceps, glutes, and hamstrings. Step forward with one leg, lower until both knees are at 90 degrees, then return to standing.",
        "muscle_groups": MuscleGroup.QUADRICEPS,
        "secondary_muscles": "glutes,hamstrings",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "equipment_required": "bodyweight",
        "category": "strength",
        "is_core_exercise": True,
        "form_analysis_available": True,
        "video_url": "/videos/lunge.mp4",
        "image_url": "/images/lunge.png",
    },
    {
        "name": "Plank",
        "description": "A core stability exercise that strengthens your entire midsection. Hold a push-up position on your forearms with a straight body line.",
        "muscle_groups": MuscleGroup.CORE,
        "secondary_muscles": "shoulders,back",
        "difficulty": DifficultyLevel.BEGINNER,
        "equipment_required": "bodyweight",
        "category": "core",
        "is_core_exercise": True,
        "form_analysis_available": True,
        "video_url": "/videos/plank.mp4",
        "image_url": "/images/plank.png",
    },
    {
        "name": "Glute Bridge",
        "description": "An exercise that targets the glutes and hamstrings. Lie on your back with knees bent, lift your hips until your body forms a straight line, then lower back down.",
        "muscle_groups": MuscleGroup.GLUTES,
        "secondary_muscles": "hamstrings,lower back",
        "difficulty": DifficultyLevel.BEGINNER,
        "equipment_required": "bodyweight",
        "category": "strength",
        "is_core_exercise": True,
        "form_analysis_available": True,
        "video_url": "/videos/glute-bridge.mp4",
        "image_url": "/images/glute-bridge.png",
    },
]

# Supporting exercises
SUPPORTING_EXERCISES_DATA = [
    {
        "name": "Bodyweight Row",
        "description": "An upper body pulling exercise using a sturdy table or bar. Targets back, biceps, and shoulders.",
        "muscle_groups": MuscleGroup.BACK,
        "secondary_muscles": "biceps",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "equipment_required": "bodyweight",
        "category": "strength",
    },
    {
        "name": "Dumbbell Shoulder Press",
        "description": "A shoulder exercise performed standing or seated. Press dumbbells overhead and lower with control.",
        "muscle_groups": MuscleGroup.SHOULDERS,
        "secondary_muscles": "triceps",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "equipment_required": "dumbbells",
        "category": "strength",
    },
    {
        "name": "Bicycle Crunch",
        "description": "A core exercise that targets obliques and rectus abdominis. Alternate bringing elbow to opposite knee while extending the other leg.",
        "muscle_groups": MuscleGroup.CORE,
        "secondary_muscles": "",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "equipment_required": "bodyweight",
        "category": "core",
    },
    {
        "name": "Jump Squat",
        "description": "A plyometric variation of the squat that builds explosive power. Squat down then jump as high as possible.",
        "muscle_groups": MuscleGroup.QUADRICEPS,
        "secondary_muscles": "glutes,calves",
        "difficulty": DifficultyLevel.ADVANCED,
        "equipment_required": "bodyweight",
        "category": "plyometric",
    },
    {
        "name": "Russian Twist",
        "description": "A core rotation exercise that targets obliques. Sit on the ground, lean back slightly, and twist your torso side to side.",
        "muscle_groups": MuscleGroup.CORE,
        "secondary_muscles": "",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "equipment_required": "bodyweight",
        "category": "core",
    },
]


async def seed_exercises(session: AsyncSession):
    """Seed the exercise library"""
    print("Seeding exercises...")

    # Check if exercises already exist
    result = await session.execute("SELECT COUNT(*) FROM exercises")
    count = result.scalar()

    if count > 0:
        print(f"✓ {count} exercises already exist, skipping seed")
        return

    # Seed core exercises
    for exercise_data in CORE_EXERCISES_DATA:
        exercise = Exercise(
            id=str(uuid.uuid4()),
            **exercise_data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(exercise)

    # Seed supporting exercises
    for exercise_data in SUPPORTING_EXERCISES_DATA:
        exercise = Exercise(
            id=str(uuid.uuid4()),
            **exercise_data,
            is_core_exercise=False,
            form_analysis_available=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(exercise)

    await session.commit()
    print(f"✓ Seeded {len(CORE_EXERCISES_DATA) + len(SUPPORTING_EXERCISES_DATA)} exercises")


async def seed_database(session: AsyncSession):
    """Seed the database with initial data"""
    print("Starting database seed...")

    await seed_exercises(session)

    print("✓ Database seed completed!")


if __name__ == "__main__":
    import asyncio

    async def main():
        from app.db.session import async_session_maker

        async with async_session_maker() as session:
            await seed_database(session)

    asyncio.run(main())
