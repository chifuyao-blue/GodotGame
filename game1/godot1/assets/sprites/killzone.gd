extends Area2D

@onready var timer = $Timer



func _on_body_entered(body):
	print("you died!") # Replace with function body.
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://savexie.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	DirAccess.remove_absolute("user://savesc1_1_2.tres")
	DirAccess.remove_absolute("user://chuan.tres")
	print("删除成功！")	
	Engine.time_scale = 0.5
	body.get_node("CollisionShape2D").queue_free()
	timer.start()

func _on_timer_timeout():
	Engine.time_scale = 1.0
	if has_saveguan2():
		get_tree().change_scene_to_file("res://scenes/game_2.tscn")
	elif has_saveguan3():
		get_tree().change_scene_to_file("res://scenes/game_3.tscn")
	else :
		get_tree().change_scene_to_file("res://game.tscn")
	#get_tree().reload_current_scene()
	
func has_saveguan2() -> bool:
	var save_path = "user://guan2.tres"
	return FileAccess.file_exists(save_path)

func has_saveguan3() -> bool:
	var save_path = "user://guan3.tres"
	return FileAccess.file_exists(save_path)
