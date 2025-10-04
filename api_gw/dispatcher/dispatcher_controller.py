from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from api_gw.db.models import Report, User
from api_gw.dto.requests import VerifyReportRequest
from api_gw.extensions import get_session

router = APIRouter()

@router.post("/dispatcher/reports/verify", response_model=Report)
def verify_report(verificationReq: VerifyReportRequest, verified: str, session: Session = Depends(get_session)):
    report = session.get(Report, verificationReq.report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    status = verificationReq.verified
    user = session.get(User, report.reporting_user_id)
    
    
    if (status == "postitive"):
        user.points += 10
        report.verified = status
    elif (status == "negative"):
        user.points -= 10
        report.verified = status
    else:
        raise HTTPException(statuss_code=400, detial="Invalid verify field. Should be positive/negative")
    session.add(user) 
    session.add(report)
    session.commit()
    session.refresh(report)
    session.add(user)
    return report