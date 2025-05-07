from typing import List, Optional
from app.database import get_supabase
from app.schemas.submission import SubmissionOut, SubmissionCreate

class SubmissionService:
    def __init__(self):
        self.supabase = get_supabase()

    async def create_submission(self, user_id: str, submission: SubmissionCreate) -> SubmissionOut:
        submission_data = submission.dict()
        submission_data["user_id"] = user_id
        
        response = self.supabase.table("submissions").insert(submission_data).execute()
        
        if not response.data:
            raise Exception("Error al crear envío")
            
        return response.data[0]

    async def get_user_submissions(self, user_id: str, exercise_id: Optional[str] = None) -> List[SubmissionOut]:
        query = self.supabase.table("submissions").select("*").eq("user_id", user_id)
        
        if exercise_id:
            query = query.eq("exercise_id", exercise_id)
            
        response = query.order("created_at", desc=True).execute()
        return response.data

    async def get_exercise_submissions(self, exercise_id: str) -> List[SubmissionOut]:
        response = self.supabase.table("submissions")\
            .select("*")\
            .eq("exercise_id", exercise_id)\
            .order("created_at", desc=True)\
            .execute()
            
        return response.data