extends Area2D
@onready var animation_player = $AnimationPlayer


@onready var label_4 = $"../../Player/ZhuangTai/TextureRect/Label4"







func _on_body_entered(_body):
	#print("ok!")
	#get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	label_4.add_point()
	animation_player.play("pick_up")
	
