#!/usr/bin/env python3
"""Roy Wong / 1% Club 千军万马 recruitment carousel (Mandarin).

A compliance-safe value post: builder-guide positioning, no income claims,
no lifestyle proof, product-and-customer before recruiting, debunks fast money.

    python3 build.py brand.json out
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: E402,F403

CJK_CSS = Path(__file__).resolve().parent / 'cjk_face.css'


def slides(brand):
    st = brand['style']

    # 1. COVER
    s1 = cover_type(['建团队这几年,', '我学到的 4 件事'], accent=1,
                    sub='想做第二收入,<br>先看完这几点。')

    # 2. 第 01 件事 — split: 一次性努力 vs 可复制系统
    wall = ('<div style="width:138px;height:166px;border-radius:calc(var(--radius) * .7);background:var(--rule);opacity:.8;padding:12px 10px">'
            + ''.join(f'<div style="height:5px;border-radius:3px;background:var(--ink-soft);opacity:.45;margin-bottom:7px;width:{w}%"></div>'
                      for w in (96, 88, 94, 80, 92, 86, 90, 70, 94, 60, 84, 76, 50)) + '</div>')
    clean = ('<div style="width:138px;height:166px;border-radius:calc(var(--radius) * .7);background:var(--paper);padding:13px 12px">'
             '<div style="font-family:var(--f-display);font-weight:var(--w-display);letter-spacing:var(--track);font-size:16px;line-height:1.12;color:var(--ink);white-space:nowrap">'
             '一个<br><span class="accent">可复制的流程</span></div>'
             '<div style="height:3px;width:70px;border-radius:2px;background:var(--accent);margin:7px 0 9px"></div>'
             + ''.join(f'<div style="display:flex;gap:6px;align-items:center;margin-bottom:6px"><span style="width:5px;height:5px;border-radius:50%;background:var(--accent)"></span>'
                       f'<div style="height:5px;border-radius:3px;background:var(--ink-soft);opacity:.5;width:{w}px"></div></div>' for w in (84, 70, 78, 66))
             + '</div>')
    s2 = section('第 01 件事', '先有系统,', '再谈规模。', [
        ('一次性的努力会累死你,', '能复制的流程才带你走远。'),
        ('把每天要做的事变成系统,', '不靠感觉,也不靠运气。'),
        ('系统会帮你记住每一步,', '不会因为你忙就断掉。'),
    ], split('一次性努力', wall, '很快见顶', '可复制系统', clean, '越走越稳'))

    # 3. 第 02 件事 — card: 想快的人 vs 想建的人
    s3 = section('第 02 件事', '我找的是会建的人,', '不是想快的人。', [
        ('想走捷径的人,', '系统留不住,他们自己也待不久。'),
        ('愿意把事做扎实的人,', '会一直在,也会带起一整队人。'),
        ('我不卖梦,', '我教你怎么把事一块一块建起来。'),
    ], card(cmd('“有没有快一点的方法?”') +
            output('有,换个地方。<br>想把事做久的,留下来一起建。<br>这里不适合只想赚快钱的人。',
                   label='我的回答', pad=(40, 13, 42), size=12),
            bar='我常被问到的一句话'))

    # 4. 第 03 件事 — flow: 客户 → 产品 → 团队
    s4 = section('第 03 件事', '先把产品和客户做好,', '团队才稳。', [
        ('产品对了,客户留下来,', '团队才有可以依靠的东西。'),
        ('先把人服务好,', '再谈招人。顺序不能反。'),
        ('把客户当长期的人,', '团队自然会跟着稳下来。'),
    ], card('<div style="padding:22px 14px 8px">' + flow([
        (ICON_CHAT, '服务<br>客户'), (ICON_SPARK, '做好<br>产品'), (ICON_PHONE, '团队<br>才稳')]) + '</div>'
        + output('顺序反了,团队就散了。<br>先有满意的客户,再谈规模。', label='为什么是这个顺序', pad=(26, 14, 28), size=12)))

    # 5. 第 04 件事 — card: 复利 not lottery
    s5 = section('第 04 件事', '结果会慢,', '但会复利。', [
        ('别信“90 天翻身”,', '真东西是复利,不是彩票。'),
        ('每天的小动作累积起来,', '半年后你会认不出自己。'),
        ('慢,不是没在动,', '是在把地基打扎实。'),
    ], card(cmd('复利 = 每天多做一点 × 时间') +
            output('不性感,也不快。<br>但这是唯一走得稳的路。<br>肯熬的人,最后都在。',
                   label='真正的玩法', pad=(40, 13, 42), size=12),
            bar='慢,但稳'))

    # 6. CTA
    s6 = cta('如果你也想建,', '不是追梦。', '建', label='私信我',
             promise='我们聊聊你可以怎么开始。',
             toolbar='看看 1% Club 千军万马怎么运作<br>结果因人而异,多数人走得更慢')
    return [s1, s2, s3, s4, s5, s6]


if __name__ == '__main__':
    brand = load_brand(sys.argv[1] if len(sys.argv) > 1 else 'brand.json')
    out = Path(sys.argv[2] if len(sys.argv) > 2 else 'out')
    extra = CJK_CSS.read_text(encoding='utf-8') if CJK_CSS.exists() else ''
    # Put the Simplified-Chinese face first on every role so CJK glyphs render.
    extra += ("\n:root{--f-display:'Noto Sans SC','Space Grotesk',sans-serif;"
              "--f-body:'Noto Sans SC','Inter',sans-serif;"
              "--f-hand:'Noto Sans SC','Inter',sans-serif;"
              "--f-mono:'Noto Sans SC','Space Mono',monospace}")
    write_carousel(out / 'carousel.html', slides(brand), brand,
                   title='建团队这几年,我学到的 4 件事', extra_css=extra)
    print('wrote', out / 'carousel.html')
