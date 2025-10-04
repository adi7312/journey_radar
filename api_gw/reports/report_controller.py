from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api_gw.db.models import Report, User
from api_gw.extensions import get_session
from api_gw.dto.requests import ReportRequest, VoteRequest
router = APIRouter()

@router.post("/reports/", response_model=Report)
def create_report(report: ReportRequest, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.id == report.reporting_user_id)).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    new_report = Report(
        likes=0,
        dislikes=0,
        verified="unverified",
        description=report.description,
        lattidude=report.lattidude,
        longidute=report.longidute,
        creator_id=report.reporting_user_id,
        route_name=report.route_name
    )
    
    session.add(new_report)
    session.commit()
    session.refresh(new_report)
    return new_report

@router.post("/reports/{report_id}/vote", response_model=Report)
def vote_report(report_id: int, vote: VoteRequest, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if vote.action == "like":
        report.likes += 1
    elif vote.action == "dislike":
        report.dislikes += 1
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'like' or 'dislike'.")
    session.add(report)
    session.commit()
    session.refresh(report)
    return report

@router.get("/reports/{report_id}", response_model=Report)
def get_report(report_id: int, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("/reports/", response_model=list[Report])
def get_all_reports(session: Session = Depends(get_session)):
    reports = session.exec(select(Report)).all()
    return reports