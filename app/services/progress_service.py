from app.database import get_supabase
from app.schemas.progress import ProgressCreate, ProgressOut

class ProgressService:
    def __init__(self):
        self.supabase = get_supabase()

    async def add_progress(self, user_id: str, progress_data: ProgressCreate) -> ProgressOut:
        data = progress_data.model_dump() if hasattr(progress_data, "model_dump") else progress_data.dict()
        data["user_id"] = user_id
        response = self.supabase.table("progress").insert(data).execute()
        if not response.data:
            raise Exception("No se pudo registrar el progreso")
        return ProgressOut(**response.data[0])

    async def get_progress(self, user_id: str):
        response = self.supabase.table("progress").select("*").eq("user_id", user_id).order("date", desc=False).execute()
        return [ProgressOut(**item) for item in response.data or []]