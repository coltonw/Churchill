from django.shortcuts import render_to_response
from django.http import HttpResponse
from bdoggle.models import Game
from bdoggle import control
import datetime, json, time

def index(request) :
    return render_to_response('bdoggle/index.html', {'game_count': Game.objects.count()})
    
#This function returns what is neccecary to start a game. 
def join_game(request) :
    games = Game.objects.all()
    game = 0;
    if not games :
        print "no games!"
        game = control.new_game()
    else :
        game = games[len(games) -1]
    if game.start_time < datetime.datetime.now() :
        game = control.new_game()
        
    if game == 0 :
        print "ERROR"
        return HttpResponse("ERROR -- No Game For You.")
    
    print time.mktime(game.start_time.utctimetuple())
    
    game_info = {
        "server_time" : time.time(),
        "number" : game.pk ,
        "start_time" : time.mktime(game.start_time.utctimetuple()),
        "board" : game.board 
    }
    
    game_info_encoded = json.dumps(game_info)
    
    return HttpResponse(game_info_encoded)