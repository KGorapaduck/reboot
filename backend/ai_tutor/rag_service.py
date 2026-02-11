from lectures.models import Lecture
from core.services import OpenAIService
from pgvector.django import L2Distance

class RAGService:
    @staticmethod
    def find_similar_lectures(query_text, limit=3):
        """
        1. Generate embedding for query text.
        2. Search DB for lectures with similar embeddings (L2 Distance).
        """
        # 1. 임베딩 생성
        query_embedding = OpenAIService.get_embedding(query_text)
        if not query_embedding:
            return []

        # 2. 벡터 검색 (pgvector L2Distance)
        # 가까운 거리(=유사한 내용) 순으로 정렬하여 상위 k개 반환
        similar_lectures = Lecture.objects.order_by(
            L2Distance('embedding', query_embedding)
        )[:limit]

        return similar_lectures

    @staticmethod
    def generate_answer(user_question, context_lectures):
        """
        Constructs a prompt with context and gets answer from GPT-4o.
        """
        context_text = "\n\n".join([
            f"Lecture: {l.title}\nContent: {l.original_script[:500]}..." 
            for l in context_lectures
        ])

        system_prompt = (
            "You are an AI Tutor for the Re:Boot coding course. "
            "Use the following lecture excerpts to answer the student's question. "
            "If the answer is not in the excerpts, say you don't know."
        )

        user_prompt = f"Context:\n{context_text}\n\nQuestion: {user_question}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return OpenAIService.chat_completion(messages)
