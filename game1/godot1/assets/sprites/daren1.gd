extends Area2D
@onready var timer_1 = $Timer1

var sc1 = 0

func _on_body_entered(body):
	
	#if sc1 == 3:
		print("you died!") # Replace with function body.
		DirAccess.remove_absolute("user://savegame.tres")
		DirAccess.remove_absolute("user://savescore.tres")
		print("删除成功！")	
		Engine.time_scale = 0.5
		body.get_node("CollisionShape2D").queue_free()
		timer_1.start()




func _on_timer_1_timeout():
	Engine.time_scale = 1.0
	get_tree().reload_current_scene()
	 # Replace with function body.
