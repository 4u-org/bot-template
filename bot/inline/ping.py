from aiogram import Router, types, F

router = Router()

@router.inline_query(F.query == "ping")
async def ping(query: types.InlineQuery):
    await query.answer(
        results=[],
        cache_time=0,
        is_personal=True,
        switch_pm_text="Pong",
        switch_pm_parameter=1
    )