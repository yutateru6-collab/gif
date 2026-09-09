from __future__ import annotations

ANIMATION_PRESETS = {
    "slash": {
        "title": "Sword Slash",
        "labels": [
            "idle-1", "idle-2", "ready-1", "ready-2",
            "step-in", "windup-1", "windup-2", "swing-start",
            "mid-slash", "full-slash", "follow-through", "impact",
            "recover-1", "recover-2", "return-1", "idle-end",
        ],
        "prompt": (
            "Create a 4x4 sprite sheet with exactly 16 frames of a pixel-art combat slash animation. "
            "Keep the character's hairstyle, outfit, colors, silhouette, and weapon consistent across all 16 frames. "
            "Motion sequence: idle stance, ready stance, step in, windup, sword slash, impact, follow-through, recovery, return to idle. "
            "Retro RPG battle style. Clear readable pose changes. Transparent or plain clean background only. "
            "Each frame must contain the same character at a consistent scale and centered position. "
            "Do not merge frames. Respect the 4x4 labeled grid."
        ),
    },
    "punch": {
        "title": "Punch Combo",
        "labels": [
            "idle-1", "idle-2", "guard-1", "guard-2",
            "shift", "jab-start", "jab-hit", "pullback",
            "cross-start", "cross-hit", "follow-through", "reset-1",
            "reset-2", "breath-1", "breath-2", "idle-end",
        ],
        "prompt": (
            "Create a 4x4 sprite sheet with exactly 16 frames of a pixel-art punch combo animation. "
            "Preserve the character identity, hairstyle, costume, colors, and body proportions. "
            "Sequence: idle, guard, weight shift, jab, recoil, cross, impact, recovery, back to idle. "
            "Retro fighting-game or RPG style, clean readable motion arcs, consistent framing, plain background. "
            "Each frame must fit cleanly inside the labeled 4x4 grid."
        ),
    },
    "spell": {
        "title": "Magic Spell",
        "labels": [
            "idle-1", "idle-2", "focus-1", "focus-2",
            "raise-hand", "charge-1", "charge-2", "charge-3",
            "cast-start", "cast-release", "burst", "linger",
            "fade-1", "recover-1", "recover-2", "idle-end",
        ],
        "prompt": (
            "Create a 4x4 sprite sheet with exactly 16 frames of a pixel-art spell-casting animation. "
            "Keep the same character design in every frame: face, clothing, palette, silhouette, and accessories. "
            "Sequence: idle, focus, raise hand or staff, gather magic, release spell, burst effect, magical afterglow, recovery, idle. "
            "Retro JRPG style with readable magic effect while keeping the character visible. Clean simple background. "
            "Respect the 4x4 grid and frame boundaries."
        ),
    },
    "jump_attack": {
        "title": "Jump Attack",
        "labels": [
            "idle-1", "crouch-1", "crouch-2", "launch",
            "rise-1", "rise-2", "air-ready", "air-attack-1",
            "air-attack-2", "air-impact", "descend-1", "descend-2",
            "land-1", "land-2", "recover", "idle-end",
        ],
        "prompt": (
            "Create a 4x4 sprite sheet with exactly 16 frames of a pixel-art jump attack animation. "
            "Maintain strict character consistency across all frames. "
            "Sequence: idle, crouch, jump launch, rise, aerial preparation, attack in the air, impact, descend, land, recover, idle. "
            "Retro side-view RPG battle animation, strong silhouette readability, consistent scale, plain background. "
            "Follow the labeled 4x4 template exactly."
        ),
    },
    "idle": {
        "title": "Idle Loop",
        "labels": [
            "idle-1", "idle-2", "idle-3", "blink-1",
            "blink-2", "idle-4", "breath-1", "breath-2",
            "breath-3", "idle-5", "idle-6", "shift-1",
            "shift-2", "idle-7", "idle-8", "idle-end",
        ],
        "prompt": (
            "Create a 4x4 sprite sheet with exactly 16 frames of a pixel-art idle animation. "
            "Same character in all frames with tiny movements only: breathing, blinking, subtle weight shift. "
            "Retro RPG sprite style, consistent centered framing, plain background, clean readable pixels. "
            "Respect the 4x4 template exactly."
        ),
    },
}


def get_preset(name: str) -> dict:
    if name not in ANIMATION_PRESETS:
        raise KeyError(f"Unknown animation preset: {name}")
    return ANIMATION_PRESETS[name]


def build_two_step_prompt() -> str:
    return (
        "Convert the provided character image into a clean retro pixel-art character sprite. "
        "Preserve the person's or character's identity, hairstyle, clothes, colors, accessories, and overall silhouette as closely as possible. "
        "Use a cute but game-ready pixel-art style with chunky readable pixels, front or near-front battle-ready standing pose, centered composition, and simple plain background. "
        "Output a single character sprite image only."
    )
