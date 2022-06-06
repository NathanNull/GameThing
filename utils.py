import pygame

def add(*tuples):
    for i in range(len(tuples)):
        if len(tuples[i]) != len(tuples[max(0, i-1)]):
            raise ValueError("Tuples are not the same length")

    return tuple([sum(v) for v in zip(*tuples)])

def mul(to_mult, factor):
    return tuple([v*factor for v in to_mult])

def lerp(start, end, amount):
    if not (0<=amount<=1):
        raise ValueError(f"Lerp amount must be between 0 and 1, got {amount}")

    return (amount * end) + ((1-amount) * start)

def get_collision_sides(rect1:pygame.Rect, rect1_last_ok:pygame.Rect, rect2:pygame.Rect):
    sides = []
    if rect1.right > rect2.left and rect1.left < rect2.right and\
        rect1_last_ok.bottom > rect2.top and rect1_last_ok.top < rect2.bottom:

        if rect1_last_ok.right <= rect2.centerx:
            sides.append("left")
        else:
            sides.append("right")

    if rect1_last_ok.right > rect2.left and rect1_last_ok.left < rect2.right and\
        rect1.bottom > rect2.top and rect1.top < rect2.bottom:

        if rect1_last_ok.bottom <= rect2.centery:
            sides.append("bottom")
        else:
            sides.append("top")

    return sides

# The original collision code I got from the internet, for reference
# if it turns out I messed up somewhere:
# https://happycoding.io/tutorials/processing/collision-detection#collision-detection-between-many-objects
# X converted: r1.r > r2.l and r1.l < r2.r and r1_b.b > r2.t and r1_b.t < r2.b
# Y converted: r1_b.r > r2.l and r1_b.l < r2.r and r1.b > r2.t and r1.t < r2.b