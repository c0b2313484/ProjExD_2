import os
import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書 
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect、または爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出していたらFalse
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出していたらFalse
        tate = False
    return yoko, tate
#rct: pg.Rect) -> tuple[bool, bool]:
def game_over():
    """
    ゲームオーバー画面を表示する関数
    ゲームアウト後に画面をブラックアウト
    Game Overの文字列表示
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bl_out = pg.Surface((WIDTH, HEIGHT))  # Surfaceを作成
    pg.draw.rect(bl_out, 0, 0, WIDTH, HEIGHT)  # ブラックアウト画面を描画
    bl_out.set_alpha((150))  # 画面を半透明にする
    screen.blit(bl_out, [1600, 900])
    fonto = pg.font.Font(None, 80)  # フォントサイズを指定
    txt = fonto.render("Game Over", True, (255, 255, 255))  # GameOverの文字描写
    screen.blit(txt, [WIDTH/2, HEIGHT/2])
    img = pg.image.load("fig/8.png")  # 画面Surface
    screen.blit(img, [WIDTH/2-200, HEIGHT/2])
    pg.display.update()
    clock = pg.time.Clock()
    clock.time(5)

def kk_chenge():
    """
    飛ぶ方向に従ってこうかとん画像を切り替える関数
    戻り値：辞書（移動量の合計値のタプル、rotezoomしたSurface)
    """
    kk_dict = {}
    DETA = {  # 押下移動量
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    return 

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bb_img = pg.Surface((20, 20))  # 20*20の黒いの範囲
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の黒い部分を透明に
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤色の円を描写
    bb_rct = bb_img.get_rect()  # 爆弾rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の中心座標にx, yの値を設定
    vx, vy = +5, +5  # 爆弾の横方向速度vx、縦方向速度vy
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # screen.blit(bg_img, [0, 0]) 
        # screen.blit(bb_img, bb_rct)  #bb_img(爆弾)をbb_rct()の位置に表示
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が衝突
            game_over()
            return  # 重なっていなければFalse
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():  # 辞書からkeyとvalueをとる
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # move_ipは爆弾を動かす
        yoko, tate  = check_bound(bb_rct)
        if not yoko:  # 爆弾が横にはみ出た場合
            vx *= -1
        if not tate:  # 爆弾が縦にはみ出た場合
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
