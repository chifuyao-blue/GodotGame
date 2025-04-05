extends Area2D

@onready var texture_rect_2 = $Player/CanvasLayer/TextureRect2
@onready var texture_rect_3 = $Player/CanvasLayer/TextureRect3
@onready var texture_rect_4 = $Player/CanvasLayer/TextureRect4


@onready var animation_player = $AnimationPlayer




var sc1 = 0
func _chupeng1():
	if sc1 == 0:
		sc1 += 1
		animation_player.play("aida1")
		texture_rect_4.hide()
	elif sc1 == 1:
		sc1 += 1
		animation_player.play("aida1")
		texture_rect_3.hide()
	elif sc1 == 2:
		animation_player.play("aida1")
		texture_rect_2.hide()
	#print("OK")
