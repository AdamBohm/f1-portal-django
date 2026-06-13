from django.shortcuts import render, get_object_or_404
from .models import Team, Driver, Track, Race

def home(request):
    # Spočítáme základy pro úvodní stranu
    stats = {
        'teams_count': Team.objects.count(),
        'drivers_count': Driver.objects.count(),
        'tracks_count': Track.objects.count(),
    }
    # Načteme všechny závody z databáze pro zobrazení kalendáře
    races = Race.objects.all()
    
    return render(request, 'f1_app/home.html', {'stats': stats, 'races': races})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'f1_app/team_list.html', {'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # Vytáhneme jezdce, kteří patří pod tento tým
    drivers = team.jezdci.all()
    return render(request, 'f1_app/team_detail.html', {'team': team, 'drivers': drivers})