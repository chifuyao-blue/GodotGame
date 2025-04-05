extends Area2D
@onready var label_6 = $"../Player3/CanvasLayer/TextureRect/Label6"
@onready var player_3 = $"../Player3"
@onready var label_7 = $Player/CanvasLayer/TextureRect/Label7
@onready var timer = $Timer
@onready var animation_player = $Label/AnimationPlayer

var sc1 = 1

func _on_body_entered(body):
	animation_player.play("tongguan2")
	timer.start()
	
func _changjing1():
	var file2 = FileAccess.open("user://savexie.tres",FileAccess.WRITE)
	file2.store_var(player_3.sc1)
	file2.store_var(player_3.xl2_1)
	file2.store_var(player_3.xl2_2)
	file2.store_var(player_3.xl2_3)
	file2.close()
	var file3 = FileAccess.open("user://savechang3.tres",FileAccess.WRITE)
	file3.store_var(sc1)
	file3.close()
	var file4 = FileAccess.open("user://savexie1_2.tres",FileAccess.WRITE)
	file4.store_var(player_3.sc1)
	file4.close()
	player_3._savesc1_1_2()


func _on_timer_timeout():
	print("第三关！！！")
	_changjing1()
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	print("删除成功！")	
	label_6._chuandi()
	get_tree().change_scene_to_file("res://scenes/game_3.tscn")
	 # Replace with function body.
