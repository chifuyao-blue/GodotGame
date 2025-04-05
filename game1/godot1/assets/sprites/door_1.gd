extends Area2D

@onready var label_4 = $"../Player/ZhuangTai/TextureRect/Label4"

@onready var player = $"../Player"
var sc1 = 1

@onready var label = $Label
@onready var animation_player = $Label/AnimationPlayer
@onready var timer = $Timer



func _on_body_entered(body):
	animation_player.play("tongguan1")
	timer.start()
	#_changjing1()
	#DirAccess.remove_absolute("user://savegame.tres")
	#DirAccess.remove_absolute("user://savescore.tres")
	#DirAccess.remove_absolute("user://saveslime.tres")
	#print("删除成功！")	
	#label_4._chuandi()
	#get_tree().change_scene_to_file("res://scenes/game_2.tscn")
	 # Replace with function body.
	
func _changjing1():
	var file2 = FileAccess.open("user://savexie.tres",FileAccess.WRITE)
	file2.store_var(player.sc1)
	file2.store_var(player.xl1)
	file2.store_var(player.xl2)
	file2.store_var(player.xl3)
	file2.close()
	var file3 = FileAccess.open("user://savechang2.tres",FileAccess.WRITE)
	file3.store_var(sc1)
	file3.close()
	var file4 = FileAccess.open("user://savexie1_2.tres",FileAccess.WRITE)
	file4.store_var(player.sc1)
	file4.close()
	player._savesc1_1_2()


func _on_timer_timeout():
	_changjing1()
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	print("删除成功！")	
	label_4._chuandi()
	get_tree().change_scene_to_file("res://scenes/game_2.tscn")
