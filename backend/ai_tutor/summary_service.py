from core.services import OpenAIService

class SummaryService:
    @staticmethod
    def summarize_script(script_segments):
        """
        Summarize the full script into sections using GPT-4o.
        Returns a markdown string.
        """
        if not script_segments:
            return ""

        # valid_segments only if content exists
        full_text = "\n".join([f"{seg['start']}-{seg['end']}: {seg['content']}" for seg in script_segments if seg.get('content')])
        
        if not full_text:
            return ""

        system_prompt = (
            "You are an expert educational content summarizer. "
            "Analyze the provided lecture transcript (with timestamps) and create a structured summary. "
            "The summary should be in Markdown format with the following structure:\n"
            "## 1. Key Concepts\n"
            "- Concept A: ...\n"
            "## 2. Detailed Summary\n"
            "- (00:00~05:00) Introduction...\n"
            "## 3. Actionable Takeaways\n"
            "- ...\n\n"
            "Keep it concise and easy to understand for students."
        )

        user_prompt = f"Here is the lecture transcript:\n\n{full_text[:30000]}" # Truncate if too long, though 4o has 128k context

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        summary = OpenAIService.chat_completion(messages)
        return summary if summary else "Summary generation failed."
    @staticmethod
    def summarize_incremental(text_chunk, existing_summary=""):
        """
        Add new information to an existing summary based on a new text chunk.
        """
        system_prompt = (
            "You are an expert educational content summarizer. "
            "You are providing a real-time summary of a lecture. "
            "Given the 'Existing Summary' and a 'New Text Chunk', update the summary to include new key points. "
            "Maintain a structured Markdown format (bullets, headers). "
            "Ensure the output is a full updated summary, not just the changes."
        )

        user_prompt = f"Existing Summary:\n{existing_summary}\n\nNew Text Chunk:\n{text_chunk}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        summary = OpenAIService.chat_completion(messages)
        return summary if summary else "Incremental summary failed."
