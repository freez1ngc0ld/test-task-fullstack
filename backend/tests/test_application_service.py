import pytest
from src.core.enums import StatusType, PriorityType
from src.features.application.exceptions import *
from src.features.application.service import ApplicationService


@pytest.mark.asyncio
async def test_create_and_get_application(app_service: ApplicationService):
    app = await app_service.create_application("Test", "Desc", StatusType.NEW, PriorityType.LOW)
    assert app.title == "Test"
    
    fetched = await app_service.get(app.id)
    assert fetched.id == app.id

@pytest.mark.asyncio
async def test_update_application(app_service: ApplicationService):
    app = await app_service.create_application("Title", "Desc", StatusType.NEW, PriorityType.LOW)
    updated = await app_service.update_application(app.id, title="New Title", status=StatusType.IN_PROGRESS, description=None, priority=None)
    
    assert updated.title == "New Title"
    assert updated.status == StatusType.IN_PROGRESS

@pytest.mark.asyncio
async def test_delete_applications(app_service: ApplicationService):
    app = await app_service.create_application("To Delete", "Desc", StatusType.NEW, PriorityType.LOW)
    result = await app_service.delete_applications([app.id])
    assert "Удалено 1" in result.status
    
    with pytest.raises(ApplicationNotFoundException):
        await app_service.get(app.id)


@pytest.mark.asyncio
async def test_get_application_fails_if_not_found(app_service: ApplicationService):
    with pytest.raises(ApplicationNotFoundException):
        await app_service.get("non-existent-id")

@pytest.mark.asyncio
async def test_update_application_fails_if_not_found(app_service: ApplicationService):
    with pytest.raises(ApplicationNotFoundException):
        await app_service.update_application("non-existent-id", "Title", None, None, None)

@pytest.mark.asyncio
async def test_update_application_fails_if_done(app_service: ApplicationService):
    app = await app_service.create_application("Done App", "Desc", StatusType.DONE, PriorityType.HIGH)

    with pytest.raises(CantTouchDoneApplicationException):
        await app_service.update_application(app.id, title="New Title", description=None, status=StatusType.NEW, priority=None)