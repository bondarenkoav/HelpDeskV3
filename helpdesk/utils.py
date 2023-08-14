

# class ProposalsLisMixin:
#     def get_queryset(self, **kwargs):
#         proposals = self.model.objects.filter(service_company=self.request.user.profile.current_scompany)
#         if self.kwargs['status'] == 'open':
#             qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__lte=datetime.today())
#         elif self.kwargs['status'] == 'scheduled':
#             qs = proposals.filter(status__slug__in=['open', 'complete'], date_schedule__gt=datetime.today())
#         else:
#             qs = proposals.filter(status__slug=self.kwargs['status'], date_schedule__year=datetime.today().year)
#         return qs