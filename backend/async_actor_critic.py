# Async actor-critic reasoning using OpenAI API and asyncio
import asyncio
import os
import openai

async def async_actor_critic_reasoning(paper_text):
    openai.api_key = os.getenv('OPENAI_API_KEY', 'sk-...')
    actor_prompt = f"[ACTOR] Summarize the main contribution of this paper:\n{paper_text[:2000]}"
    critic_prompt = "[CRITIC] Critique the following summary for accuracy and completeness:"
    try:
        actor_resp = await asyncio.to_thread(
            lambda: openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": actor_prompt}]
            )
        )
        actor_summary = actor_resp.choices[0].message.content.strip()
        critic_resp = await asyncio.to_thread(
            lambda: openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": critic_prompt + "\n" + actor_summary}]
            )
        )
        critic_review = critic_resp.choices[0].message.content.strip()
    except Exception as e:
        actor_summary = critic_review = f"Error: {e}"
    return {'actor': actor_summary, 'critic': critic_review, 'model': 'gpt-4o'}
