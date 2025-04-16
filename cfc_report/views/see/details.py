from django.shortcuts import render, get_object_or_404

from cfc_report.models import Tournament


def tournament_detail(request, pk):
    """
    View for displaying the details of a specific tournament.
    """
    tournament = get_object_or_404(Tournament, id=pk)
    context = {
        "tournament": tournament,
    }
    return render(request, "cfc_report/show/tournament_detail.html", context)
