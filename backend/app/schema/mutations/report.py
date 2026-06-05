import graphene
from app.models import db, Report
from app.schema.types import ReportType

class CreateReport(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)
        type = graphene.String(required=True)
        report_link = graphene.String(required=True)

    report = graphene.Field(ReportType)

    def mutate(self, info, user_id, start_date, end_date, type, report_link):
        new_report = Report(user_id=user_id, start_date=start_date, end_date=end_date, type=type, report_link=report_link)
        db.session.add(new_report)
        db.session.commit()
        return CreateReport(report=new_report)
