extends "res://assets/sprites/coinKZ.gd"


# Called when the node enters the scene tree for the first time.
func _ready():
	#hide()
	#set_monitoring(false)  # 禁用碰撞检测
   

	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
func _on_body_entered(_body):
	#print("ok!")
	#get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	label_4.add_point()
	label_4._co2()
	#get_tree().change_scene_to_file("res://scenes/game_2.tscn")
	animation_player.play("pick_up")
