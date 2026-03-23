#!/usr/bin/env python3
"""Generate a glowing tea-pet frog SVG based on recent commit count.

Usage: python generate_pet.py <commit_count> > teapet.svg
"""

import sys


def lerp(a, b, t):
    return a + (b - a) * t


def hex_color(r1, g1, b1, r2, g2, b2, t):
    r = int(lerp(r1, r2, t))
    g = int(lerp(g1, g2, t))
    b = int(lerp(b1, b2, t))
    return f"#{r:02x}{g:02x}{b:02x}"


def steam_wisp(cx, base_y, dur, delay):
    return f"""  <path d="M {cx} {base_y} Q {cx+9} {base_y-14} {cx} {base_y-28} Q {cx-9} {base_y-42} {cx} {base_y-56}"
        stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0">
      <animate attributeName="opacity" values="0;0.55;0" dur="{dur}" begin="{delay}" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate"
        values="0,0; 4,-6; 0,-12" dur="{dur}" begin="{delay}" repeatCount="indefinite"/>
    </path>"""


def generate_svg(commits: int, max_commits: int = 30) -> str:
    t = min(commits / max_commits, 1.0)

    # ── aura ──────────────────────────────────────────────────────────────────
    aura_rx   = lerp(28,  85, t)
    aura_ry   = lerp(12,  42, t)
    glow_min  = lerp(0.00, 0.18, t)
    glow_max  = lerp(0.04, 0.72, t)

    # ── eye colour: dark brown → bright green ─────────────────────────────────
    eye_hex   = hex_color(0x22, 0x10, 0x06, 0x00, 0xff, 0x55, t)
    eye_glow  = lerp(0.0, 0.95, t)

    # ── body colour brightens slightly ────────────────────────────────────────
    hi  = hex_color(0xc4, 0x7a, 0x4a, 0xd6, 0x9e, 0x62, t)
    shd = hex_color(0x8b, 0x5e, 0x3c, 0x70, 0x4e, 0x30, t)

    # ── steam ─────────────────────────────────────────────────────────────────
    steam_count = 0 if t < 0.40 else (1 if t < 0.70 else 3)
    steam_svg   = ""
    if steam_count >= 1:
        steam_svg += steam_wisp(100, 72, "2.4s", "0s")
    if steam_count >= 3:
        steam_svg += steam_wisp(84,  78, "2.0s", "0.7s")
        steam_svg += steam_wisp(116, 76, "2.8s", "1.3s")

    return f"""<svg width="200" height="235" viewBox="0 0 200 235"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Breathing aura glow -->
    <radialGradient id="aura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#44ff88">
        <animate attributeName="stop-opacity"
          values="{glow_max:.3f};{glow_min:.3f};{glow_max:.3f}"
          dur="3s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#44ff88" stop-opacity="0"/>
    </radialGradient>

    <!-- Body gradient -->
    <radialGradient id="body" cx="36%" cy="28%" r="68%">
      <stop offset="0%"   stop-color="{hi}"/>
      <stop offset="100%" stop-color="{shd}"/>
    </radialGradient>

    <!-- Per-eye glow gradients -->
    <radialGradient id="egl" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="{eye_hex}" stop-opacity="{eye_glow:.3f}"/>
      <stop offset="100%" stop-color="{eye_hex}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="egr" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="{eye_hex}" stop-opacity="{eye_glow:.3f}"/>
      <stop offset="100%" stop-color="{eye_hex}" stop-opacity="0"/>
    </radialGradient>

    <filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="blur5"><feGaussianBlur stdDeviation="5"/></filter>
  </defs>

  <!-- Ground aura -->
  <ellipse cx="100" cy="200" rx="{aura_rx:.1f}" ry="{aura_ry:.1f}"
    fill="url(#aura)" filter="url(#blur5)"/>

  <!-- Ground shadow -->
  <ellipse cx="100" cy="207" rx="46" ry="8" fill="#000" opacity="0.18"/>

  <!-- Steam wisps -->
{steam_svg}

  <!-- ── Tea pet body (layered back → front) ── -->

  <!-- Back legs -->
  <ellipse cx="61"  cy="191" rx="30" ry="14" fill="url(#body)"
    transform="rotate(-18 61 191)"/>
  <ellipse cx="139" cy="191" rx="30" ry="14" fill="url(#body)"
    transform="rotate(18 139 191)"/>

  <!-- Main body -->
  <ellipse cx="100" cy="165" rx="51" ry="39" fill="url(#body)"/>

  <!-- Front legs -->
  <ellipse cx="67"  cy="178" rx="19" ry="10" fill="url(#body)"
    transform="rotate(-22 67 178)"/>
  <ellipse cx="133" cy="178" rx="19" ry="10" fill="url(#body)"
    transform="rotate(22 133 178)"/>

  <!-- Neck -->
  <ellipse cx="100" cy="137" rx="26" ry="13" fill="url(#body)"/>

  <!-- Head -->
  <circle cx="100" cy="116" r="35" fill="url(#body)"/>

  <!-- Eye bumps -->
  <circle cx="83"  cy="100" r="14" fill="url(#body)"/>
  <circle cx="117" cy="100" r="14" fill="url(#body)"/>

  <!-- Eye glow halos -->
  <circle cx="83"  cy="100" r="20" fill="url(#egl)" filter="url(#blur3)"/>
  <circle cx="117" cy="100" r="20" fill="url(#egr)" filter="url(#blur3)"/>

  <!-- Pupils -->
  <circle cx="83"  cy="100" r="7.5" fill="{eye_hex}"/>
  <circle cx="117" cy="100" r="7.5" fill="{eye_hex}"/>

  <!-- Eye shine -->
  <circle cx="80"  cy="97"  r="2.8" fill="white" opacity="0.85"/>
  <circle cx="114" cy="97"  r="2.8" fill="white" opacity="0.85"/>

  <!-- Smile -->
  <path d="M 88 124 Q 100 133 112 124"
    stroke="{shd}" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Nostrils -->
  <circle cx="96"  cy="119" r="2.2" fill="{shd}" opacity="0.55"/>
  <circle cx="104" cy="119" r="2.2" fill="{shd}" opacity="0.55"/>

</svg>"""


if __name__ == "__main__":
    commits = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print(generate_svg(commits))
