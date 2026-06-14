from __future__ import annotations

import json
from pathlib import Path
import unittest

from tools.import_assassin_sample import read_png


ROOT = Path(__file__).resolve().parents[1]


class WebStaticTests(unittest.TestCase):
    def frame_pixels(
        self, pixels: bytearray, sheet_width: int, frame_width: int, frame_height: int, row: int, col: int
    ) -> bytearray:
        frame = bytearray(frame_width * frame_height * 4)
        for y in range(frame_height):
            src_start = ((row * frame_height + y) * sheet_width + col * frame_width) * 4
            dst_start = y * frame_width * 4
            frame[dst_start:dst_start + frame_width * 4] = pixels[src_start:src_start + frame_width * 4]
        return frame

    def pixel_difference(self, left: bytearray, right: bytearray) -> int:
        return sum(abs(a - b) for a, b in zip(left, right))

    def alpha_bbox(self, pixels: bytearray, width: int, height: int) -> tuple[int, int, int, int] | None:
        min_x = width
        min_y = height
        max_x = -1
        max_y = -1
        for y in range(height):
            for x in range(width):
                if pixels[(y * width + x) * 4 + 3] <= 8:
                    continue
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
        if max_x < 0:
            return None
        return min_x, min_y, max_x + 1, max_y + 1

    def monster_body_anchor_bbox(
        self, pixels: bytearray, width: int, height: int
    ) -> tuple[int, int, int, int] | None:
        body = bytearray(pixels)
        for index in range(0, len(body), 4):
            if body[index + 3] <= 8:
                continue
            r, g, b = body[index], body[index + 1], body[index + 2]
            brightness = (r + g + b) / 3
            saturation = max(r, g, b) - min(r, g, b)
            if brightness > 225 or (brightness > 185 and saturation > 85):
                body[index + 3] = 0
        return self.alpha_bbox(body, width, height)

    def frame_region_pixels(
        self,
        pixels: bytearray,
        sheet_width: int,
        frame_width: int,
        frame_height: int,
        row: int,
        col: int,
        y0: int,
        y1: int,
    ) -> bytearray:
        region = bytearray()
        for y in range(y0, min(frame_height, y1)):
            src_start = ((row * frame_height + y) * sheet_width + col * frame_width) * 4
            region.extend(pixels[src_start:src_start + frame_width * 4])
        return region


    def test_character_creation_controls_exist(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")

        for marker in (
            "profileGate",
            "characterNameInput",
            "genderMaleButton",
            "genderFemaleButton",
            "rollTalentButton",
            "confirmCharacterButton",
            "attackSpeedText",
            "hpRegenText",
            "expText",
            "expProgressBar",
            "reviveText",
            "stageLoading",
            "stageLoadingText",
            "equipmentSlotList",
            "newCharacterButton",
        ):
            self.assertIn(marker, html)

    def test_frontend_renders_system_shop_recycling_and_donation_controls(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "systemShopList",
            "recycleAllButton",
        ):
            self.assertIn(marker, html)

        for marker in (
            "renderSystemShop",
            "SYSTEM_SHOP_TRANSLATIONS",
            "systemShopDisplayName",
            "systemShopDescription",
            "systemShopPreviewHtml",
            "systemShopPreviewItem",
            "/system-shop/buy",
            "/inventory/recycle",
            "/inventory/recycle-all",
            "/market/sell-to-system",
            "/talent/donate",
            "sell-to-system",
            "expand-talent",
            "rainbow",
        ):
            self.assertIn(marker, script)

    def test_frontend_has_account_login_and_three_character_slots(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "accountPanel",
            "accountUsernameInput",
            "accountPasswordInput",
            "loginButton",
            "registerButton",
            "characterSlotList",
            "logoutButton",
        ):
            self.assertIn(marker, html)

        for marker in (
            "SESSION_STORAGE_KEY",
            "MAX_CHARACTER_SLOTS",
            "renderCharacterSlots",
            "refreshAccount",
            "/account/login",
            "/account/register",
            "/characters/select",
            "/characters/delete",
            "X-Session-Token",
        ):
            self.assertIn(marker, script)

    def test_frontend_uses_continuous_visual_motion(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("advanceVisualState", script)
        self.assertIn("snapVisualStateToSnapshot", script)
        self.assertIn("visualSnapshot", script)
        self.assertIn("VISUAL_SNAP_DISTANCE", script)
        self.assertIn("renderScene(visualSnapshot()", script)
        self.assertNotIn("interpolateEntity", script)
        self.assertNotIn("applyVisualPrediction", script)

    def test_frontend_uses_ultra_smooth_motion_loop(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("SIMULATION_STEP_SECONDS = 0.125", script)
        self.assertIn("SIMULATION_TICK_MS = 125", script)
        self.assertIn("VISUAL_MAX_FRAME_DELTA_MS = 500", script)
        self.assertIn("advanceVisualState", script)
        self.assertIn("applyCameraDamping", script)
        self.assertIn("drawBlendedSpriteBottom", script)
        self.assertIn("return (x - cameraX) * worldScale + 56", script)
        self.assertIn("Math.min(VISUAL_MAX_FRAME_DELTA_MS", script)

    def test_mobile_runtime_throttles_tick_and_render_work(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("MOBILE_SIMULATION_STEP_SECONDS = 0.5", script)
        self.assertIn("MOBILE_SIMULATION_TICK_MS = 500", script)
        self.assertIn("MOBILE_RENDER_FRAME_MS = 1000 / 30", script)
        self.assertIn("function isMobileRuntime()", script)
        self.assertIn("function simulationStepSeconds()", script)
        self.assertIn("function simulationTickMs()", script)
        self.assertIn("function renderFrameBudgetMs()", script)
        self.assertIn("function shouldThrottleRenderFrame(timestamp)", script)
        self.assertIn("if (shouldThrottleRenderFrame(timestamp))", script)
        self.assertIn("function syncSimulationTimer(", script)
        self.assertIn("simulationCadenceKey()", script)
        self.assertIn("window.setInterval(() => tick(cadence.stepSeconds), cadence.tickMs)", script)

    def test_desktop_window_width_does_not_enable_mobile_tick_cadence(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        start = script.index("function isMobileRuntime()")
        end = script.index("function simulationStepSeconds()", start)
        mobile_body = script[start:end]

        self.assertIn("window.matchMedia('(pointer: coarse)')", mobile_body)
        self.assertIn("navigator.maxTouchPoints", mobile_body)
        self.assertNotIn("max-width", mobile_body)

    def test_resize_resynchronizes_runtime_tick_cadence(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("tickCadenceKey: null", script)
        self.assertIn("function handleViewportRuntimeChange()", script)
        self.assertIn("state.lastPaintAt = 0", script)
        self.assertIn("syncSimulationTimer()", script)
        self.assertIn("window.addEventListener('resize', handleViewportRuntimeChange)", script)
        self.assertIn("document.addEventListener('visibilitychange', handleViewportRuntimeChange)", script)

    def test_sprite_animation_does_not_crossfade_transparent_frames(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function drawBlendedSpriteBottom", script)
        self.assertNotIn("ctx.globalAlpha = 1 - amount", script)
        self.assertNotIn("ctx.globalAlpha = amount", script)

    def test_hero_uses_skeleton_equipment_anchors(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("createHeroSkeleton", script)
        self.assertIn("entity.gender === 'female'", script)
        self.assertIn("drawHeroBackHair", script)
        self.assertIn("drawHeroHair", script)
        self.assertIn("drawHeroEye", script)
        self.assertIn("rightHand", script)
        self.assertIn("leftHand", script)
        self.assertIn("mainHand", script)
        self.assertIn("offHand", script)
        self.assertIn("drawHeroRig", script)
        self.assertIn("drawEquippedWeapon", script)
        self.assertIn("drawWeaponOnHand", script)
        self.assertNotIn("ctx.translate(x + 15, y - 45)", script)

    def test_female_hair_stays_behind_face_and_eye(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function drawHeroHead(")
        end = script.index("function drawHeroBackHair", start)
        body = script[start:end]

        self.assertLess(body.index("drawHeroBackHair"), body.index("ctx.ellipse(skeleton.head.x"))
        self.assertLess(body.index("ctx.ellipse(skeleton.head.x"), body.index("drawHeroHair"))
        self.assertLess(body.index("drawHeroHair"), body.index("drawHeroEye"))
        self.assertNotIn("skeleton.head.x + 9, skeleton.head.y + 3", script)

    def test_monster_sprites_face_hero_without_forced_flip(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function drawMonster(")
        end = script.index("function drawTreasureMimic", start)
        body = script[start:end]

        self.assertIn("monsterFacingFlip(entity)", script)
        self.assertIn("function monsterFacingFlip(entity)", script)
        self.assertNotIn("width, height, true, frames[2]", body)
        self.assertNotIn("width, height, true)", body)
        self.assertIn("String(sprite.key || '').startsWith('pixelMonster')", script)

    def test_safe_monster_generator_exists_for_complete_sprite_sheets(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        generator = (ROOT / "tools" / "generate_safe_monster_assets.py").read_text(encoding="utf-8")

        self.assertIn("return PIXEL_SPRITES.monsters[exact]", script)
        self.assertNotIn("PIXEL_MONSTER_STABLE_ACTIONS", script)
        self.assertIn("Generate complete fixed-slot monster sprite sheets", generator)
        self.assertIn("write_sheet(MONSTER_ROOT", generator)

    def test_attack_range_guide_does_not_draw_hand_dashed_line(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function drawCombatRange(")
        end = script.index("function drawAssetBackground", start)
        body = script[start:end]

        self.assertNotIn("setLineDash", body)
        self.assertNotIn("ctx.lineTo(end", body)

    def test_hero_health_bar_draws_above_rig_and_weapon(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function drawHero(")
        end = script.index("function createHeroSkeleton", start)
        body = script[start:end]

        self.assertIn("drawHeroHealthBar", script)
        self.assertLess(body.index("drawHeroRig"), body.index("drawEquippedWeapon"))
        self.assertLess(body.index("drawEquippedWeapon"), body.index("drawHeroHealthBar"))
        self.assertIn("function heroHealthBarAnchor(", script)
        self.assertIn("haloAnchorFromSkeleton(skeleton)", script)
        self.assertIn("Math.min(head.y - 92, halo.y - 26)", script)
        self.assertNotIn("skeleton.head.y - 24", script)

    def test_pixel_art_sprite_manifest_and_assets_exist(self) -> None:
        manifest_path = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        for key in ("male_base", "female_base"):
            asset = manifest["heroes"][key]
            image_path = ROOT / asset["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(asset["frameWidth"], 96)
            self.assertEqual(asset["frameHeight"], 96)
            self.assertIn("mainHand", asset["anchors"])

        assassin = manifest["heroes"]["male_assassin"]
        self.assertEqual(
            assassin["image"],
            "/web/assets/pixel/v1/heroes/male/pixellab_shadow_assassin.png",
        )
        assassin_path = ROOT / assassin["image"].lstrip("/")
        self.assertTrue(assassin_path.exists(), assassin_path)
        self.assertEqual(assassin_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        male_width, male_height, _male_pixels = read_png(assassin_path)
        self.assertEqual(assassin["frameWidth"], 128)
        self.assertEqual(assassin["frameHeight"], 128)
        self.assertEqual(male_width, assassin["frameWidth"] * 15)
        self.assertEqual(male_height, assassin["frameHeight"] * 11)
        self.assertGreaterEqual(assassin["drawWidth"], 108)
        self.assertIn("attack_blade", assassin["animations"])
        self.assertEqual(assassin["animations"]["walk"]["frames"], 15)
        self.assertEqual(assassin["animations"]["attack_blade"]["frames"], 9)
        self.assertEqual(assassin["animations"]["attack_dual"]["frames"], 9)

        female_assassin = manifest["heroes"]["female_assassin"]
        self.assertEqual(
            female_assassin["image"],
            "/web/assets/pixel/v1/heroes/female/pixellab_shadow_assassin.png",
        )
        female_assassin_path = ROOT / female_assassin["image"].lstrip("/")
        self.assertTrue(female_assassin_path.exists(), female_assassin_path)
        self.assertEqual(female_assassin_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        female_width, female_height, _female_pixels = read_png(female_assassin_path)
        self.assertEqual(female_assassin["frameWidth"], 128)
        self.assertEqual(female_assassin["frameHeight"], 128)
        self.assertEqual(female_width, female_assassin["frameWidth"] * 16)
        self.assertEqual(female_height, female_assassin["frameHeight"] * 11)
        self.assertGreaterEqual(female_assassin["drawWidth"], 108)
        self.assertIn("attack_blade", female_assassin["animations"])
        self.assertIn("mainHand", female_assassin["anchors"])
        self.assertEqual(female_assassin["animations"]["idle"]["frames"], 5)
        self.assertEqual(female_assassin["animations"]["walk"]["frames"], 12)
        self.assertEqual(female_assassin["animations"]["attack_blade"]["frames"], 9)
        self.assertEqual(female_assassin["animations"]["hurt"]["frames"], 5)

        for key in ("slime", "thorn", "imp", "forest_boss"):
            asset = manifest["monsters"][key]
            image_path = ROOT / asset["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn("animations", asset)
            self.assertEqual(asset["source"], "pixellab")

        for key in ("forest", "deep_forest"):
            asset = manifest["maps"][key]
            image_path = ROOT / asset["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            width, height, _pixels = read_png(image_path)
            self.assertEqual(width, asset["width"])
            self.assertEqual(height, asset["height"])
            self.assertEqual(asset["source"], "pixellab")

    def test_female_assassin_has_distinct_silhouette_from_male_assassin(self) -> None:
        male_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "assassin_sample.png"
        female_path = (
            ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "female" / "pixellab_shadow_assassin.png"
        )
        male_width, male_height, male_pixels = read_png(male_path)
        female_width, female_height, female_pixels = read_png(female_path)

        self.assertEqual(female_height, male_height)
        self.assertGreater(female_width, male_width)
        alpha_difference = sum(
            1
            for row in range(male_height)
            for col in range(male_width)
            if (male_pixels[(row * male_width + col) * 4 + 3] > 0)
            != (female_pixels[(row * female_width + col) * 4 + 3] > 0)
        )

        self.assertGreater(alpha_difference, 2000)

    def test_male_assassin_is_not_the_old_cutout_model(self) -> None:
        old_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "assassin_sample.png"
        new_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "pixellab_shadow_assassin.png"
        old_width, _old_height, old_pixels = read_png(old_path)
        new_width, _new_height, new_pixels = read_png(new_path)

        old_idle = self.frame_pixels(old_pixels, old_width, 128, 128, 0, 0)
        new_idle = self.frame_pixels(new_pixels, new_width, 128, 128, 0, 0)
        old_alpha = [
            old_idle[(row * 128 + col) * 4 + 3] > 0
            for row in range(128)
            for col in range(128)
        ]
        new_alpha = [
            new_idle[(row * 128 + col) * 4 + 3] > 0
            for row in range(128)
            for col in range(128)
        ]
        alpha_difference = sum(1 for old, new in zip(old_alpha, new_alpha) if old != new)

        self.assertGreater(alpha_difference, 2500)

    def test_female_assassin_faces_right_and_uses_action_poses(self) -> None:
        female_path = (
            ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "female" / "pixellab_shadow_assassin.png"
        )
        width, _height, pixels = read_png(female_path)
        frame_width = 128
        frame_height = 128
        idle = self.frame_pixels(pixels, width, frame_width, frame_height, 0, 0)
        walk = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 3)
        attack = self.frame_pixels(pixels, width, frame_width, frame_height, 3, 5)

        face_pixels = []
        for y in range(64):
            for x in range(frame_width):
                index = (y * frame_width + x) * 4
                r, g, b, a = idle[index:index + 4]
                if a > 80 and r > 150 and g > 70 and b > 70 and r > g + 15 and r > b + 15:
                    face_pixels.append(x)

        self.assertGreater(len(face_pixels), 80)
        self.assertGreater(sum(face_pixels) / len(face_pixels), 64)
        self.assertGreater(self.pixel_difference(idle, walk), 80000)
        self.assertGreater(self.pixel_difference(idle, attack), 80000)

    def test_frontend_does_not_fake_pixel_walk_with_overlay(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertNotIn("drawPixelWalkStrideCue", script)
        self.assertNotIn("pixelHeroWalkPose", script)

    def test_female_assassin_walk_has_distinct_lower_body_from_attack(self) -> None:
        female_path = (
            ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "female" / "pixellab_shadow_assassin.png"
        )
        width, _height, pixels = read_png(female_path)
        frame_width = 128
        frame_height = 128

        for frame in range(2, 7):
            walk_legs = self.frame_region_pixels(pixels, width, frame_width, frame_height, 1, frame, 64, 128)
            attack_legs = self.frame_region_pixels(pixels, width, frame_width, frame_height, 3, frame, 64, 128)
            self.assertGreater(self.pixel_difference(walk_legs, attack_legs), 90000)

    def test_pixellab_helper_supports_skeleton_estimation(self) -> None:
        helper = (ROOT / "tools" / "pixellab_api_generate.py").read_text(encoding="utf-8")

        self.assertIn("cmd_estimate_skeleton", helper)
        self.assertIn('"/estimate-skeleton"', helper)
        self.assertIn('subparsers.add_parser("estimate-skeleton"', helper)
        self.assertIn("cmd_animate_skeleton", helper)
        self.assertIn('"/animate-with-skeleton"', helper)
        self.assertIn('subparsers.add_parser("animate-skeleton"', helper)

    def test_female_assassin_uses_pixellab_skeleton_frame_anchors(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("FEMALE_ASSASSIN_FRAME_ANCHORS", script)
        self.assertIn("frameAnchors: FEMALE_ASSASSIN_FRAME_ANCHORS", script)
        self.assertIn("function heroFrameSkeletonAnchorPoints(", script)
        self.assertIn("heroFrameSkeletonAnchorPoints(actionName, frame, sprite)", script)
        self.assertIn("'attack_blade'", script)
        self.assertIn("attack_dual", script)
        self.assertIn("[[104.6, 36.3, 0.08]", script)

    def test_male_assassin_uses_pixellab_walk_and_attack_skeleton_frame_anchors(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("MALE_ASSASSIN_ACTIONS", script)
        self.assertIn("walk: { row: 1, frames: 15, frameMs: 48 }", script)
        self.assertIn("attack_blade: { row: 3, frames: 9, frameMs: 48 }", script)
        self.assertIn("attack_dual: { row: 4, frames: 9, frameMs: 46 }", script)
        self.assertIn("MALE_ASSASSIN_FRAME_ANCHORS", script)
        self.assertIn("frameAnchors: MALE_ASSASSIN_FRAME_ANCHORS", script)
        self.assertIn("actions: MALE_ASSASSIN_ACTIONS", script)
        self.assertIn("[[90.3,68.1,0.84]", script)
        self.assertIn("[[84.4,71.2,1.21]", script)
        self.assertIn("[[69.1,19.2,-2.11]", script)
        self.assertIn("[[69.1,19.2,-2.11],[30.7,25.6,-2.45]", script)

    def test_male_assassin_attack_rows_have_readable_key_poses(self) -> None:
        male_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "pixellab_shadow_assassin.png"
        width, _height, pixels = read_png(male_path)
        frame_width = 128
        frame_height = 128

        blade_start = self.frame_pixels(pixels, width, frame_width, frame_height, 3, 0)
        blade_mid = self.frame_pixels(pixels, width, frame_width, frame_height, 3, 4)
        dual_start = self.frame_pixels(pixels, width, frame_width, frame_height, 4, 0)
        dual_mid = self.frame_pixels(pixels, width, frame_width, frame_height, 4, 4)

        self.assertGreater(self.pixel_difference(blade_start, blade_mid), 250000)
        self.assertGreater(self.pixel_difference(dual_start, dual_mid), 250000)

    def test_male_assassin_walk_keeps_pixellab_tail_frames(self) -> None:
        male_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "pixellab_shadow_assassin.png"
        width, _height, pixels = read_png(male_path)
        frame_width = 128
        frame_height = 128

        tail = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 11)
        final = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 12)

        self.assertGreater(self.pixel_difference(tail, final), 25000)

    def test_male_assassin_walk_has_pixellab_loop_bridge_frames(self) -> None:
        male_path = ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "male" / "pixellab_shadow_assassin.png"
        width, _height, pixels = read_png(male_path)
        frame_width = 128
        frame_height = 128

        first = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 0)
        old_final = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 12)
        bridge_one = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 13)
        bridge_two = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 14)

        self.assertGreater(self.pixel_difference(old_final, bridge_one), 25000)
        self.assertGreater(self.pixel_difference(bridge_one, bridge_two), 25000)
        self.assertLess(self.pixel_difference(bridge_two, first), self.pixel_difference(old_final, first))

    def test_pixel_hero_base_is_weaponless_and_supports_weapon_actions(self) -> None:
        generator = (ROOT / "tools" / "generate_pixel_assets.py").read_text(encoding="utf-8")
        manifest = json.loads(
            (ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json").read_text(
                encoding="utf-8"
            )
        )

        for animation in (
            "attack_unarmed",
            "attack_blade",
            "attack_dual",
            "attack_bow",
            "attack_spear",
            "attack_heavy",
        ):
            self.assertIn(animation, manifest["heroes"]["male_base"]["animations"])
            self.assertIn(animation, manifest["heroes"]["female_base"]["animations"])
            self.assertIn(animation, manifest["heroes"]["female_assassin"]["animations"])

        self.assertNotIn("f1e7c4", generator)
        self.assertNotIn("right_hand[0] + 22", generator)

    def test_frontend_selects_pixel_attack_animation_from_weapon_type(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "function heroWeaponProfile(",
            "function weaponAnimationType(",
            "function heroEquipmentAnchorsForFrame(",
            "entity.gender === 'female'",
            "weaponProfile && weaponProfile.dual ? 'attack_dual' : 'attack_blade'",
            "rawType.includes('dual') || rawType.includes('dagger_pair')",
            "dual: Boolean(offhand) || type === 'dual'",
            "attackProgress",
            "attackEase",
            "attack_bow",
            "attack_dual",
            "attack_spear",
            "attack_heavy",
            "attack_blade",
            "attack_unarmed",
        ):
            self.assertIn(marker, script)

        weapon_start = script.index("function drawEquippedWeapon(")
        weapon_end = script.index("function drawBowOnHands", weapon_start)
        weapon_body = script[weapon_start:weapon_end]
        self.assertLess(
            weapon_body.index("drawWeaponOnHand(skeleton.offHand"),
            weapon_body.index("drawWeaponOnHand(skeleton.mainHand"),
        )

    def test_frontend_cache_busts_pixel_asset_paths(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('/web/app.js?v=assassin-v82', html)
        self.assertIn('/web/styles.css?v=assassin-v82', html)
        self.assertIn("PIXEL_ASSET_VERSION", script)
        self.assertIn("assassin-v82", script)
        self.assertIn("?v=${PIXEL_ASSET_VERSION}", script)

    def test_static_files_are_served_without_browser_cache(self) -> None:
        server = (ROOT / "server.py").read_text(encoding="utf-8")

        self.assertIn('self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")', server)
        self.assertIn('self.send_header("Pragma", "no-cache")', server)
        self.assertIn('self.send_header("Expires", "0")', server)

    def test_stage_loading_waits_for_current_hero_sprite_before_revealing_canvas(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="stageLoading"', html)
        self.assertIn('class="stage-loading hidden"', html)
        self.assertIn("stageLoadToken: 0", script)
        self.assertIn("function stageAssetKeysForSnapshot(", script)
        self.assertIn("equipmentAssetKey(equipmentAppearance(item))", script)
        self.assertIn("return Array.from(new Set(keys))", script)
        self.assertIn("gender === 'female' ? 'pixelHeroFemaleAssassin' : 'pixelHeroMaleAssassin'", script)
        self.assertIn("function waitForStageAssets(", script)
        self.assertIn("const assetLoadPromises = {}", script)
        self.assertIn("Promise.allSettled(", script)
        self.assertIn("state.assetsReady = true", script)
        self.assertIn("function updateStageLoading()", script)
        self.assertIn("state.stageReady = Boolean(state.assetsReady && state.snapshot && state.visual.ready)", script)
        self.assertIn("waitForStageAssets(snapshot, stageLoadToken)", script)
        self.assertIn("if (state.stageLoadToken !== token)", script)
        self.assertIn("canvas.setAttribute('aria-busy'", script)
        self.assertIn(".stage-loading", styles)
        self.assertIn("loading_rune_loop.png?v=assassin-v53", styles)
        self.assertIn("animation: stage-loading-rune 0.86s steps(8) infinite", styles)
        self.assertIn("@keyframes stage-loading-rune", styles)
        self.assertIn("background-position: -768px 0", styles)
        self.assertNotIn("backdrop-filter: blur", styles)

        loading_asset = ROOT / "web" / "assets" / "pixel" / "v1" / "ui" / "loading_rune_loop.png"
        self.assertTrue(loading_asset.exists(), loading_asset)
        width, height, _pixels = read_png(loading_asset)
        self.assertEqual(width, 64 * 8)
        self.assertEqual(height, 64)

    def test_rift_entry_prewarms_backgrounds_without_blocking_rift_entry(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("const RIFT_BACKGROUND_PRELOAD_ASSET_KEYS = [", script)
        for key in [
            "bgCave",
            "bgCastle",
            "bgSky",
            "bgClouds",
            "groundStone",
            "blockStone",
            "brickGrey",
        ]:
            self.assertIn(f"'{key}'", script)
        self.assertIn("const RIFT_COMBAT_PRELOAD_ASSET_KEYS = [", script)
        for key in [
            "pixelSlime",
            "pixelThorn",
            "pixelImp",
            "pixelForestBoss",
            "talentRiftEffect",
        ]:
            self.assertIn(f"'{key}'", script)
        self.assertIn("const assetDecodePromises = {}", script)
        self.assertIn("function decodeAssetImage(key)", script)
        self.assertIn("image.decode ? image.decode().catch(() => null) : Promise.resolve(null)", script)
        self.assertIn("function warmAssetKeys(keys)", script)
        self.assertIn("function warmRiftAssets()", script)
        self.assertIn("...RIFT_BACKGROUND_PRELOAD_ASSET_KEYS", script)
        self.assertIn("...RIFT_COMBAT_PRELOAD_ASSET_KEYS", script)
        self.assertIn("function scheduleRiftAssetWarmup()", script)
        self.assertIn("window.requestIdleCallback || ((callback) => window.setTimeout(callback, 250))", script)
        self.assertIn("function beginStageAssetTransition(snapshot)", script)
        self.assertIn("waitForStageAssets(snapshot, token)", script)
        self.assertIn("decodeAssetImage(key)", script)
        self.assertIn("if (options.prepareStageAssets)", script)
        self.assertIn("beginStageAssetTransition(snapshot)", script)
        self.assertIn("warmRiftAssets()", script)
        self.assertIn(
            "postAction('/rift/enter', { floor: snapshot.rift.unlocked_floor }, t('enterRift'))",
            script,
        )
        self.assertIn(
            "postAction('/rift/auto', { enabled: !autoRift }, autoRift ? t('autoRiftOff') : t('autoRiftOn'))",
            script,
        )
        start = script.index("els.enterRiftButton.addEventListener")
        end = script.index("els.leaveRiftButton.addEventListener", start)
        rift_handlers = script[start:end]
        self.assertNotIn("prepareStageAssets", rift_handlers)
        self.assertIn("scheduleRiftAssetWarmup()", script)
        start = script.index("function stageAssetKeysForSnapshot(")
        end = script.index("function waitForStageAssets(", start)
        stage_body = script[start:end]
        self.assertNotIn("RIFT_BACKGROUND_PRELOAD_ASSET_KEYS", stage_body)
        self.assertNotIn("RIFT_COMBAT_PRELOAD_ASSET_KEYS", stage_body)
        self.assertNotIn("RIFT_PRELOAD_ASSET_KEYS", stage_body)

    def test_frontend_uses_pixel_sprite_renderer_with_fallback(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        hero_start = script.index("function drawHero(")
        hero_end = script.index("function createHeroSkeleton", hero_start)
        hero_body = script[hero_start:hero_end]
        monster_start = script.index("function drawMonster(")
        monster_end = script.index("function monsterFacingFlip", monster_start)
        monster_body = script[monster_start:monster_end]

        self.assertIn("PIXEL_SPRITES", script)
        self.assertIn("drawSpriteSheetFrameBottom", script)
        self.assertIn("drawPixelHero", script)
        self.assertIn("male_assassin", script)
        self.assertIn("female_assassin", script)
        self.assertIn("pixelHeroMaleAssassin", script)
        self.assertIn("pixelHeroFemaleAssassin", script)
        self.assertIn("entity.gender === 'female' ? 'female_assassin' : 'male_assassin'", script)
        self.assertIn("drawPixelMonster", script)
        self.assertLess(hero_body.index("drawPixelHero"), hero_body.index("drawHeroRig"))
        self.assertIn("if (!drewPixelHero)", hero_body)
        self.assertIn("drawPixelMonster", monster_body)

    def test_frontend_renders_spiritual_overlays_for_premium_assassin_sample(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        hero_start = script.index("function drawHero(")
        hero_end = script.index("function createHeroSkeleton", hero_start)
        hero_body = script[hero_start:hero_end]

        self.assertNotIn("equipmentMode: 'weapon_only'", script)
        self.assertIn("drawEquippedFootCircle", hero_body)
        self.assertIn("drawEquippedWings", hero_body)
        self.assertIn("drawEquippedHalo", hero_body)
        self.assertIn("drawRingPet", hero_body)

    def test_mobile_creation_gate_can_scroll_to_roll_controls(self) -> None:
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        media_start = styles.index("@media (max-width: 860px)")
        media_body = styles[media_start:]

        self.assertIn("overflow-y: auto", styles[styles.index(".profile-gate") : styles.index(".profile-gate.hidden")])
        self.assertIn(".profile-gate", media_body)
        self.assertIn("align-items: flex-start", media_body)
        self.assertIn("max-height: none", media_body)

    def test_talent_list_has_own_scroll_region_for_expanded_talents(self) -> None:
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        start = styles.index(".talent-list {")
        end = styles.index("}", start)
        talent_body = styles[start:end]

        self.assertIn("max-height: min(42vh, 360px)", talent_body)
        self.assertIn("overflow: auto", talent_body)
        self.assertIn("padding-right: 4px", talent_body)

    def test_talent_evolve_buttons_lock_while_request_is_in_flight(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("talentEvolutionInFlight: false", script)
        self.assertIn("function evolveTalent(button)", script)
        self.assertIn("if (state.talentEvolutionInFlight)", script)
        self.assertIn("state.talentEvolutionInFlight = true", script)
        self.assertIn("state.talentEvolutionInFlight = false", script)
        self.assertIn("button.disabled = true", script)
        self.assertIn("renderCurrentTalents()", script)

    def test_frontend_renders_exp_revive_and_equipment_slots(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("expText", script)
        self.assertIn("expProgressBar", script)
        self.assertIn("reviveText", script)
        self.assertIn("renderEquipmentSlots", script)
        self.assertIn("equipment_slots", script)
        self.assertIn("reviving", script)
        self.assertIn("复活中", script)

    def test_high_frequency_snapshots_throttle_expensive_panel_renders(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "equipmentSlotsRenderSignature: ''",
            "equippedRenderSignature: ''",
            "talentsRenderSignature: ''",
            "eventsRenderSignature: ''",
            "function renderEquipmentSlots(slots, equipped, force = true)",
            "function renderEquipped(equipped, force = true)",
            "function renderTalents(talents, scrolls, talentMeta, force = true)",
            "function renderEvents(events, force = true)",
            "renderEquipmentSlots(hero.equipment_slots || [], hero.equipped || {}, false)",
            "renderEquipped(hero.equipped || {}, false)",
            "renderTalents(hero.talents || [], hero.talent_scrolls || 0, snapshot.talent || {}, false)",
            "renderEvents(snapshot.events || [], false)",
        ):
            self.assertIn(marker, script)

    def test_tick_loop_accumulates_seconds_while_request_is_in_flight(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("tickQueuedSeconds: 0", script)
        self.assertIn("state.tickQueuedSeconds += Math.max(0, Number(seconds) || 0)", script)
        self.assertIn("const queuedSeconds = Math.min(1, state.tickQueuedSeconds)", script)
        self.assertIn("state.tickQueuedSeconds = Math.max(0, state.tickQueuedSeconds - queuedSeconds)", script)
        self.assertIn("window.setTimeout(() => tick(queuedSeconds), 0)", script)

    def test_tick_requests_have_timeout_to_recover_from_stalled_updates(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("TICK_REQUEST_TIMEOUT_MS = 4000", script)
        self.assertIn("const controller = options.timeoutMs ? new AbortController() : null", script)
        self.assertIn("window.setTimeout(() => controller.abort(), options.timeoutMs)", script)
        self.assertIn("signal: controller ? controller.signal : undefined", script)
        self.assertIn("timeoutId && window.clearTimeout(timeoutId)", script)
        self.assertIn("timeoutMs: TICK_REQUEST_TIMEOUT_MS", script)

    def test_frontend_retries_read_fetches_after_transient_network_failure(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("NETWORK_RETRY_DELAY_MS = 180", script)
        self.assertIn("function isReadRequest(options = {})", script)
        self.assertIn("function isTransientFetchError(error)", script)
        self.assertIn("function fetchWithNetworkRetry(path, request, options)", script)
        self.assertIn("return fetchWithNetworkRetry(path, request, options)", script)
        self.assertIn("if (!isReadRequest(options) || !isTransientFetchError(error))", script)
        self.assertIn("window.setTimeout(resolve, NETWORK_RETRY_DELAY_MS)", script)

    def test_frontend_hides_raw_failed_to_fetch_messages(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function userFacingErrorMessage(error, fallbackKey = 'actionFail')", script)
        self.assertIn("message.includes('failed to fetch')", script)
        self.assertIn("message.includes('networkerror')", script)
        self.assertIn("message.includes('abort')", script)
        self.assertIn("return t(fallbackKey)", script)
        self.assertIn("setStatus(userFacingErrorMessage(error), false)", script)
        self.assertIn("setAccountStatus(userFacingErrorMessage(error, 'profileInvalid'), false)", script)

    def test_visual_state_interpolates_snapshot_targets(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "visualTarget",
            "spawnVisualPosition",
            "approachVisualPosition",
            "entity.visualTarget",
            "next.position.x = approachVisualPosition(",
            "lerp(currentX, targetX, amount)",
            "if (next.type === 'hero' && movingEntity(next))",
            "shouldSkipMovingEntityLerp(entity)",
        ):
            self.assertIn(marker, script)

    def test_mode_or_rift_run_change_resets_visual_camera_before_applying_snapshot(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function applySnapshot(snapshot)")
        end = script.index("function describeRiftState", start)
        body = script[start:end]

        self.assertIn("function riftRunKey(snapshot)", script)
        self.assertIn("function shouldResetVisualForSnapshot(previousSnapshot, nextSnapshot)", script)
        self.assertIn("return `${rift.floor || 0}:${rift.theme || ''}:${rift.started_tick || 0}`", script)
        self.assertIn("const shouldResetVisual = shouldResetVisualForSnapshot(state.snapshot, snapshot)", body)
        self.assertIn("if (shouldResetVisual)", body)
        self.assertIn("resetVisualSmoothing()", body)
        self.assertLess(body.index("resetVisualSmoothing()"), body.index("snapVisualStateToSnapshot(snapshot)"))

    def test_frontend_draws_equipped_models_and_item_previews(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        for marker in (
            "equipmentAppearance(",
            "equipmentPreviewHtml",
            "EQUIPMENT_MODEL_ASSET_KEYS",
            "equipmentAssetPath(appearance)",
            "equipmentSpriteImage(appearance)",
            "drawEquipmentSprite(appearance",
            "drawWingEquipmentSprite",
            "drawEquippedWings",
            "drawEquippedHalo",
            "drawEquippedFootCircle",
            "drawRingPet",
            "drawEquipmentGlow",
            "drawWeaponOnHand(skeleton.mainHand, equipped.weapon",
        ):
            self.assertIn(marker, script)

        self.assertIn("equipmentPreviewHtml(item)", script)
        self.assertIn("const wingFlap = Math.sin", script)
        self.assertIn("haloAnchorFromSkeleton(skeleton)", script)
        self.assertIn("const verticalGap = skeleton.frameBased ? 72 : 42", script)
        self.assertIn("drawHaloBurst(anchor, palette, haloSpin", script)
        self.assertIn("drawFootAuraOrbit(anchor, palette, auraSpin", script)
        self.assertIn("const petHop = Math.sin", script)
        self.assertIn("scaleX: 1 + petSquash", script)
        self.assertIn("gear-has-image", script)
        self.assertIn("gear-preview", styles)
        self.assertIn("--gear-image", styles)
        self.assertIn("gear-core", styles)
        self.assertIn("gear-edge", styles)
        self.assertIn("display: none", styles)

    def test_pixellab_equipment_model_assets_exist_and_are_wired(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        manifest = json.loads(
            (ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json").read_text(
                encoding="utf-8"
            )
        )
        expected = {
            "wooden_blade": (96, 96),
            "blade": (96, 96),
            "axe": (96, 96),
            "spear": (96, 96),
            "visor_helm": (96, 96),
            "crown_helm": (96, 96),
            "leather_mail": (160, 96),
            "plate_mail": (160, 96),
            "travel_boots": (128, 96),
            "winged_boots": (128, 96),
            "sprout_pet": (64, 64),
            "leaf_pet": (64, 64),
            "moon_cat_pet": (64, 64),
            "star_bunny_pet": (64, 64),
            "spark_fox_pet": (64, 64),
            "ember_fox_pet": (64, 64),
        }

        self.assertEqual(set(manifest["equipment"]), set(expected))
        for model, (expected_width, expected_height) in expected.items():
            asset = manifest["equipment"][model]
            self.assertEqual(asset["width"], expected_width)
            self.assertEqual(asset["height"], expected_height)
            path = ROOT / asset["image"].lstrip("/")
            self.assertTrue(path.exists(), path)
            width, height, pixels = read_png(path)
            self.assertEqual(width, expected_width)
            self.assertEqual(height, expected_height)
            visible_pixels = sum(1 for index in range(3, len(pixels), 4) if pixels[index] > 0)
            self.assertGreater(visible_pixels, 20, model)
            self.assertIn(f"/web/assets/pixel/v1/equipment/{model}.png", script)
            self.assertIn(model, script)

    def test_premium_equipment_overlays_are_spiritual_shapes_not_body_armor(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "function drawEquippedHalo(",
            "function drawEquippedWings(",
            "function drawEquippedFootCircle(",
            "skeleton.halo",
            "skeleton.back",
            "skeleton.feetCenter",
            "drawRarityParticle(anchors[slot] || skeleton.torso, item, slot)",
        ):
            self.assertIn(marker, script)

        self.assertNotIn("function drawEquippedArmor(", script)
        self.assertNotIn("function drawEquippedHelmet(", script)
        self.assertNotIn("function drawEquippedBoots(", script)

    def test_premium_assassin_equipment_anchor_calibration(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        manifest = json.loads(
            (ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json").read_text(
                encoding="utf-8"
            )
        )
        anchors = manifest["heroes"]["male_assassin"]["anchors"]

        self.assertEqual(anchors["mainHand"], [90, 68])
        self.assertEqual(anchors["offHand"], [28, 73])
        self.assertEqual(anchors["ringHand"], [28, 73])
        self.assertEqual(anchors["halo"], [73, 0])
        self.assertEqual(anchors["back"], [34, 40])
        self.assertEqual(anchors["feetCenter"], [57, 125])
        self.assertIn("const ASSASSIN_EQUIPMENT_ANCHORS", script)
        self.assertIn("offHandDrift", script)
        self.assertIn("attackProgress", script)
        self.assertIn("attackEase", script)
        self.assertIn("-1.35 + attackEase * 1.7", script)
        self.assertIn("function ringPetAnchor(", script)
        self.assertIn("skeleton.ringHand || skeleton.offHand", script)
        self.assertIn("ring: ringPetAnchor(skeleton.ringHand || skeleton.offHand)", script)
        self.assertIn("radiusX = boots.rarity === 'red' ? 34", script)
        self.assertIn("drawWingEdgeGlow(anchor, palette, armor.rarity, spread, lift)", script)

    def test_ring_slot_is_presented_as_following_pet(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("\\u6212\\u6307\\u5ba0\\u7269", script)
        self.assertIn("ring: 'Ring Pet'", script)
        self.assertIn("function drawRingPet(", script)
        self.assertIn("function ringPetAnchor(", script)
        self.assertIn("drawPetBody(", script)
        self.assertIn("gear-slot-ring-pet", styles)

    def test_frontend_draws_talent_auras_and_loot_floaters(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "state.lootFloaters",
            "state.seenLootEventKeys",
            "trackLootFloaters",
            "drawLootFloaters",
            "lootFloatText",
            "item_name",
            "+1 ",
            "drawTalentAura",
            "talentAuraStyle",
            "move_speed_pct",
            "drawLightningAura",
        ):
            self.assertIn(marker, script)

    def test_system_shop_display_uses_translated_item_copy(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("\\u6350\\u8d60\\u5370\\u8bb0", script)
        self.assertIn("\\u68f1\\u5f69\\u5229\\u5203", script)
        self.assertIn("systemShopDisplayName(entry)", script)
        self.assertIn("systemShopDescription(entry)", script)
        self.assertNotIn("escapeHtml(entry.name || entry.sku)</span>", script)
        self.assertNotIn("escapeHtml(entry.description || '')", script)

    def test_pixellab_talent_effect_assets_exist_and_are_wired(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json").read_text(encoding="utf-8"))

        for name in (
            "talent_lightning",
            "talent_flame",
            "talent_dragon",
            "talent_ward",
            "talent_vigor",
            "talent_treasure",
            "talent_gold",
            "talent_exp",
            "talent_mimic",
            "talent_rift",
        ):
            path = ROOT / "web" / "assets" / "pixel" / "v1" / "effects" / f"{name}.png"
            self.assertTrue(path.exists(), name)
            width, height, pixels = read_png(path)
            self.assertEqual((width, height), (128, 128))
            self.assertGreater(sum(pixels[3::4]), 0, name)
            self.assertIn(name, manifest["effects"])

        for marker in (
            "talentLightningEffect",
            "talentFlameEffect",
            "talentDragonEffect",
            "talentWardEffect",
            "talentVigorEffect",
            "talentTreasureEffect",
            "talentGoldEffect",
            "talentExpEffect",
            "talentMimicEffect",
            "talentRiftEffect",
            "drawPixellabTalentAura",
            "talentAuraStyles",
            "talentStyleForEffect",
        ):
            self.assertIn(marker, script)

    def test_frontend_draws_gold_loss_floaters(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("gold_loss", script)
        self.assertIn("isLootFloatEvent", script)
        self.assertIn("goldLossFloatText", script)
        self.assertIn("gold_lost", script)
        self.assertIn("rarity: lootFloatRarity(event)", script)

    def test_pixellab_equipment_effect_asset_exists_and_is_wired(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json").read_text(encoding="utf-8"))
        path = ROOT / "web" / "assets" / "pixel" / "v1" / "effects" / "equipment_enchant.png"

        self.assertTrue(path.exists())
        width, height, pixels = read_png(path)
        self.assertEqual((width, height), (128, 128))
        self.assertGreater(sum(pixels[3::4]), 0)
        self.assertIn("equipment_enchant", manifest["effects"])
        self.assertIn("equipmentEnchantEffect", script)
        self.assertIn("drawPixellabEquipmentEffect", script)
        self.assertIn("drawPixellabEquipmentEffect(anchors[slot]", script)

    def test_wing_effects_use_gem_particles_instead_of_body_ring(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        wing_body = script.split("function drawEquippedWings(", 1)[1].split("function drawEquippedHalo(", 1)[0]

        self.assertIn("function drawWingEdgeGlow(", script)
        self.assertIn("function drawWingGemParticles(", script)
        self.assertIn("function drawGemParticle(", script)
        self.assertIn("drawWingEdgeGlow(anchor, palette, armor.rarity, spread, lift)", wing_body)
        self.assertIn("drawWingGemParticles(anchor, palette, armor.rarity, spread, wingWidth, wingHeight)", script)
        self.assertIn("rarity === 'rainbow' ? 30 : rarity === 'red' ? 22", script)
        self.assertIn("if (slot === 'armor')", script)
        self.assertNotIn("drawEquipmentGlow(", wing_body)
        self.assertNotIn("armor: 1.02", script)
        self.assertNotIn("armor: { x: -6, y: -12 }", script)

    def test_frontend_draws_attack_and_rarity_particle_effects(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "state.attackEffects",
            "state.seenAttackEventKeys",
            "trackAttackEffects",
            "drawAttackEffects",
            "attackEffectProfile",
            "drawWeaponRarityBurst",
            "drawEquippedParticleEffects",
            "purple",
            "gold",
            "red",
        ):
            self.assertIn(marker, script)

    def test_frontend_renders_deep_forest_controls_and_scene(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("deepenForestButton", html)
        self.assertIn("retreatForestButton", html)
        for marker in (
            "/forest/deepen",
            "/forest/retreat",
            "deep_forest",
            "drawDeepForestCanopy",
            "monsterThreatStyle",
            "forest_depth",
            "forest.recommended_power",
        ):
            self.assertIn(marker, script)

    def test_frontend_renders_auto_rift_control(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="autoRiftButton"', html)
        self.assertIn("autoRiftButton: document.querySelector('#autoRiftButton')", script)
        self.assertIn("autoRiftOn", script)
        self.assertIn("autoRiftOff", script)
        self.assertIn("Boolean(rift.auto)", script)
        self.assertIn("els.autoRiftButton.classList.toggle('active', autoRift)", script)
        self.assertIn("postAction('/rift/auto', { enabled: !autoRift },", script)

    def test_frontend_has_settings_pause_volume_and_language(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for marker in (
            "settingsButton",
            "settingsPanel",
            "pauseToggle",
            "volumeSlider",
            "languageSelect",
        ):
            self.assertIn(marker, html)

        for marker in (
            "SETTINGS_STORAGE_KEY",
            "state.settings",
            "applySettings",
            "togglePause",
            "setMasterVolume",
            "loadEquipmentTranslations",
            "translateItemName",
            "translateEventMessage",
        ):
            self.assertIn(marker, script)

    def test_equipment_translation_table_supports_chinese_and_english(self) -> None:
        translations = json.loads((ROOT / "web" / "i18n" / "equipment.json").read_text(encoding="utf-8"))

        self.assertIn("Starter Wooden Sword", translations)
        self.assertEqual(translations["Starter Wooden Sword"]["zh-CN"], "新手木剑")
        self.assertEqual(translations["Starter Wooden Sword"]["en-US"], "Starter Wooden Sword")

    def test_frontend_displays_move_speed_stat(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("moveSpeedText", html)
        self.assertIn("hero.speed", script)
        self.assertIn("moveSpeed", script)

    def test_frontend_scales_movement_visuals_with_speed(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("movementIntensity", script)
        self.assertIn("drawMovementTrail", script)

    def test_walk_animation_is_distance_driven(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("WALK_PIXELS_PER_FRAME", script)
        self.assertIn("WALK_PIXELS_PER_FRAME = 4", script)
        self.assertIn("WALK_FRAME_SEQUENCE", script)
        self.assertIn("WALK_FRAME_SEQUENCE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]", script)
        self.assertIn("walk: { row: 1, frames: 12, frameMs: 44 }", script)
        self.assertNotIn("WALK_FRAME_SEQUENCE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12", script)
        self.assertNotIn("[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]", script)
        self.assertIn("function walkFrameSequence(", script)
        self.assertIn("visualWalkDistance", script)
        self.assertIn("next.visualWalkDistance = Number(current.visualWalkDistance || 0)", script)
        self.assertIn("function walkCycleFrame(", script)
        self.assertIn("walkCycleFrame(entity, frameCount)", script)
        self.assertIn("spriteSheetFrameInfo(sprite, actionName, entity)", script)
        self.assertNotIn("frame: Math.floor((state.lastRenderAt || 0) / frameMs) % frameCount", script)

    def test_background_scroll_uses_continuous_visual_camera(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("pixelBackgroundForest", script)
        self.assertIn("pixelBackgroundDeepForest", script)
        self.assertIn("function drawPixelForestBackground(", script)
        self.assertIn("drawPixelForestBackground(biome, width, height)", script)
        self.assertIn("visualCameraOffset", script)
        self.assertIn("cameraTargetX", script)
        self.assertIn("function visualCameraTarget(", script)
        self.assertIn("const cameraTargetX = visualCameraTarget(hero, speed, seconds, heroVisualStep)", script)
        self.assertIn("advanceMovingVisualCamera(cameraTargetX)", script)
        self.assertIn("HERO_CAMERA_LEAD_SECONDS", script)
        self.assertIn("HERO_CAMERA_MAX_LEAD", script)
        self.assertIn("HERO_CAMERA_MAX_LAG", script)
        self.assertIn("const fallbackCameraStep = speed * Math.max(0, seconds)", script)
        self.assertIn("const nextCameraX = state.visual.cameraX + cameraStep", script)
        self.assertIn("syncCameraToHeroBounds(nextCameraX, heroX, followOffset)", script)
        self.assertIn("function syncCameraToHeroBounds(", script)
        self.assertNotIn("heroX - HERO_CAMERA_OFFSET + lead", script)
        self.assertNotIn("snapshotTargetX + VISUAL_SNAP_DISTANCE", script)
        self.assertIn("const visualCameraX = visualCameraOffset(cameraX)", script)
        self.assertIn("drawGround(biome, width, height, groundY, visualCameraX, worldScale)", script)
        self.assertIn("drawDecorations(scene.decorations || [], visualCameraX", script)
        self.assertNotIn("applyCameraDamping(Math.max(0, Number(hero.position.x || 0) - 180)", script)

    def test_rift_camera_uses_same_follow_offset_as_forest(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("const RIFT_CAMERA_OFFSET = HERO_CAMERA_OFFSET", script)
        self.assertIn("function cameraFollowOffset()", script)
        self.assertIn("state.snapshot && state.snapshot.mode === 'rift'", script)
        self.assertIn("return RIFT_CAMERA_OFFSET", script)
        self.assertIn("return HERO_CAMERA_OFFSET", script)
        self.assertIn("function syncCameraToHeroBounds(cameraX, heroX, followOffset = HERO_CAMERA_OFFSET)", script)
        self.assertIn("const center = Math.max(0, heroX - followOffset)", script)
        self.assertIn("const followOffset = cameraFollowOffset()", script)
        self.assertIn("syncCameraToHeroBounds(nextCameraX, heroX, followOffset)", script)

    def test_pixellab_monsters_do_not_get_extra_canvas_aura(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        pixel_block = script.split("const drewPixelMonster = drawPixelMonster", 1)[1].split("const drewMonster =", 1)[0]

        self.assertIn("if (drewPixelMonster)", pixel_block)
        self.assertIn("return", pixel_block)
        self.assertNotIn("drawMonsterThreatOverlay", pixel_block)
        self.assertNotIn("ctx.ellipse", pixel_block)

    def test_pixellab_monster_health_bar_uses_sprite_height(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function pixelMonsterDrawSize(entity, sprite = null)", script)
        self.assertIn("const pixelSize = pixelMonsterDrawSize(entity)", script)
        self.assertIn("const healthWidth = pixelSize ? Math.max(52 * scale, pixelSize.drawWidth * 0.62) : 52 * scale", script)
        self.assertIn("const healthY = pixelSize ? y - flightLift + 5 - pixelSize.drawHeight - (boss ? 14 : 10) : y - 60 * scale", script)
        self.assertIn("drawHealthBar(x - healthWidth / 2, healthY, healthWidth, 7", script)

    def test_frontend_tracks_rift_transition_timing(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("riftTransition: null", script)
        self.assertIn("function startRiftTransitionTrace(action)", script)
        self.assertIn("function markRiftTransitionTrace(stage)", script)
        self.assertIn("function finishRiftTransitionTrace(stage)", script)
        self.assertIn("startRiftTransitionTrace('enter')", script)
        self.assertIn("startRiftTransitionTrace('auto')", script)
        self.assertIn("state.riftTransition.firstVisualHeroMoveAt", script)
        self.assertIn("state.riftTransition.firstVisualCameraMoveAt", script)
        self.assertIn("markRiftTransitionTrace('request-start')", script)
        self.assertIn("markRiftTransitionTrace('response-received')", script)
        self.assertIn("markRiftTransitionTrace('snapshot-applied')", script)
        self.assertIn("finishRiftTransitionTrace('visual-ready')", script)
        self.assertIn("riftTransition: state.riftTransition", script)

    def test_frontend_can_show_rift_transition_debug_panel(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="riftDebugPanel"', html)
        self.assertIn('id="riftDebugText"', html)
        self.assertIn("riftDebugPanel: document.querySelector('#riftDebugPanel')", script)
        self.assertIn("riftDebugText: document.querySelector('#riftDebugText')", script)
        self.assertIn("riftDebugEnabled: false", script)
        self.assertIn("new URLSearchParams(window.location.search).get('debug') === 'rift'", script)
        self.assertIn("function updateRiftDebugPanel(debug)", script)
        self.assertIn("formatDebugMs(durations.firstVisualHeroMoveMs)", script)
        self.assertIn("formatDebugMs(durations.firstVisualCameraMoveMs)", script)
        self.assertIn(".rift-debug-panel", styles)
        self.assertIn(".rift-debug-panel.hidden", styles)

    def test_moving_entities_do_not_lerp_back_to_stale_snapshots(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function shouldSkipMovingEntityLerp(", script)
        self.assertIn("if (shouldSkipMovingEntityLerp(entity))", script)
        self.assertIn("if (next.type === 'hero' && movingEntity(next))", script)
        self.assertIn("continue", script)

    def test_combat_transition_keeps_visual_approach_until_hero_reaches_range(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function transitioningIntoCombatRange(", script)
        self.assertIn("next.visualCombatApproach = true", script)
        self.assertIn("hero.visualCombatApproach", script)
        self.assertIn("if (entity.visualCombatApproach) return 'walk'", script)
        self.assertIn("function combatVisualRangeGrace(", script)
        self.assertIn("Math.max(COMBAT_VISUAL_RANGE_GRACE, range * 0.45)", script)
        self.assertIn("function visibleMonsterWithinAttackRange(", script)
        self.assertIn("const visualGrace = combatVisualRangeGrace(hero)", script)
        self.assertIn("monsterX - heroX <= Math.max(0, range) + visualGrace", script)
        self.assertIn("if (visibleMonsterWithinAttackRange(current, currentMonster))", script)
        self.assertIn("return false", script)
        self.assertIn("clearVisualCombatApproach(hero, monster)", script)
        self.assertIn("if (visibleMonsterWithinAttackRange(hero, monster))", script)

    def test_frontend_exposes_readonly_visual_debug_state(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("window.__idleForestDebug = function idleForestDebug()", script)
        self.assertIn("function updateIdleForestDebugDataset()", script)
        self.assertIn("document.documentElement.dataset.idleDebug", script)
        self.assertIn("updateIdleForestDebugDataset()", script)
        self.assertIn("gameReady: state.gameReady", script)
        self.assertIn("tickInFlight: state.tickInFlight", script)
        self.assertIn("tickQueuedSeconds: Number(state.tickQueuedSeconds.toFixed(3))", script)
        self.assertIn("tickTimerActive: Boolean(state.tickTimer)", script)
        self.assertIn("visualHeroState: visualHero && visualHero.state", script)
        self.assertIn("visualHeroScreenX", script)
        self.assertIn("visualMonsterScreenX", script)
        self.assertIn("visualScreenDistance", script)
        self.assertIn("snapshotScreenDistance", script)
        self.assertIn("worldScale", script)
        self.assertIn("visualCombatApproach: Boolean(visualHero && visualHero.visualCombatApproach)", script)
        self.assertIn("combatVisualGrace: visualHero ? combatVisualRangeGrace(visualHero) : null", script)

    def test_moving_camera_integrates_without_frame_damping(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function advanceMovingVisualCamera(", script)
        self.assertIn("state.visual.cameraX = state.visual.cameraTargetX", script)
        self.assertIn("advanceMovingVisualCamera(cameraTargetX)", script)
        self.assertIn("advanceRestingVisualCamera(cameraTargetX, seconds)", script)
        self.assertNotIn("targetX + VISUAL_SNAP_DISTANCE", script)

    def test_female_assassin_walk_loop_repeats_first_frame_as_last(self) -> None:
        female_path = (
            ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "female" / "pixellab_shadow_assassin.png"
        )
        width, _height, pixels = read_png(female_path)
        frame_width = 128
        frame_height = 128
        first = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 0)
        last = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 11)

        self.assertLess(self.pixel_difference(first, last), 450000)

    def test_female_assassin_walk_loop_starts_on_stride_pose(self) -> None:
        female_path = (
            ROOT / "web" / "assets" / "pixel" / "v1" / "heroes" / "female" / "pixellab_shadow_assassin.png"
        )
        width, _height, pixels = read_png(female_path)
        frame_width = 128
        frame_height = 128
        idle_legs = self.frame_region_pixels(pixels, width, frame_width, frame_height, 0, 0, 64, 128)
        first_legs = self.frame_region_pixels(pixels, width, frame_width, frame_height, 1, 0, 64, 128)
        penultimate = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 10)
        closing = self.frame_pixels(pixels, width, frame_width, frame_height, 1, 11)

        self.assertGreater(self.pixel_difference(first_legs, idle_legs), 250000)
        self.assertLess(self.pixel_difference(penultimate, closing), 650000)

    def test_monster_visual_spawn_buffer_keeps_monsters_offscreen(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("MONSTER_SPAWN_SCREEN_BUFFER = 820", script)
        self.assertNotIn("MONSTER_VISUAL_SPAWN_AHEAD = 260", script)

    def test_forest_ground_uses_smooth_low_frequency_scroll(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function drawSmoothGroundTexture(", script)
        self.assertIn("if (drawSmoothGroundTexture(biome, width, height, groundY, cameraX, worldScale))", script)
        self.assertIn("cameraX * worldScale * 0.35", script)
        self.assertIn("groundScuffSpacing", script)

    def test_frontend_uses_listing_price_dialog(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("listingPanel", html)
        self.assertIn("listingPriceInput", html)
        self.assertIn("listingConfirmButton", html)
        self.assertIn("listingCancelButton", html)
        self.assertIn("listingDraftItemId", script)
        self.assertIn("openListingPanel", script)
        self.assertIn("closeListingPanel", script)
        self.assertIn("invalidPrice", script)
        self.assertIn(".listing-panel", styles)
        self.assertNotIn("window.prompt", script)

    def test_frontend_keeps_market_buttons_stable_between_ticks(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("inventoryRenderSignature", script)
        self.assertIn("marketRenderSignature", script)
        self.assertIn("marketActionInFlightIds", script)
        self.assertIn("inventorySignature", script)
        self.assertIn("marketSignature", script)
        self.assertIn("renderInventory(hero.inventory || [], false)", script)
        self.assertIn("renderMarket((snapshot.market && snapshot.market.active) || [], hero.id, false)", script)

    def test_frontend_renders_cancel_button_for_own_market_listing(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function renderMarket(")
        end = script.index("function renderEvents", start)
        body = script[start:end]

        self.assertIn("data-action=\"cancel-listing\"", body)
        self.assertIn("/market/cancel", script)
        self.assertIn("cancelListing", script)

    def test_frontend_persists_local_character(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("idleForestProfile", script)
        self.assertIn("/profile/roll", script)
        self.assertIn("/profile/confirm", script)

    def test_frontend_uses_account_session_before_showing_login(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function bootstrapProfile()")
        end = script.index("function applySnapshot", start)
        body = script[start:end]

        self.assertIn("loadSessionToken()", body)
        self.assertIn("refreshAccount()", body)
        self.assertIn("accountState.authenticated", body)
        self.assertIn("accountState.active_character_id", body)
        self.assertIn("api('/snapshot')", body)
        self.assertLess(body.index("loadSessionToken()"), body.index("refreshAccount()"))
        self.assertLess(body.index("accountState.active_character_id"), body.index("api('/snapshot')"))

    def test_frontend_registration_stays_on_character_slots_before_entering_game(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function submitAccount(")
        end = script.index("function refreshAccount", start)
        body = script[start:end]

        self.assertIn("const isRegister = path.includes('register')", body)
        self.assertIn("if (result.active_character_id && !isRegister)", body)
        self.assertIn("showCharacterPanel()", body)
        self.assertIn("showCreationPanel()", body)

    def test_frontend_resumes_simulation_when_starting_game(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        start = script.index("function startGame(")
        end = script.index("function stopGameLoop", start)
        body = script[start:end]

        self.assertIn("state.settings.paused = false", body)
        self.assertIn("saveSettings()", body)

    def test_pixellab_monster_roster_assets_exist_and_are_wired(self) -> None:
        manifest_path = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        sprite_records = [
            "forest_slime",
            "thorn_boar",
            "moss_imp",
            "wild_mushroom",
            "bark_guard",
            "cave_bat",
            "crystal_lurker",
            "stone_crawler",
            "cloud_wisp",
            "storm_harpy",
            "sun_mote",
            "rust_guard",
            "hollow_knight",
            "cursed_squire",
        ]
        deep_aliases = ["shadow_slime", "bramble_wolf", "gloom_imp", "venom_mushroom", "ancient_bark_guard"]
        bosses = ["cave_warden", "tempest_seraph", "throne_keeper"]
        monsters = manifest["monsters"]

        for key in sprite_records:
            self.assertIn(key, monsters)
            record = monsters[key]
            self.assertEqual(record["frameWidth"], 64)
            self.assertEqual(record["frameHeight"], 64)
            self.assertEqual(record["source"], "pixellab")
            self.assertEqual(set(record["animations"]), {"idle", "walk", "attack", "hurt", "death"})
            image_path = ROOT / record["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn(key, script)

        for key in deep_aliases:
            self.assertIn(key, script)

        for key in bosses:
            self.assertIn(key, monsters)
            record = monsters[key]
            self.assertEqual(record["frameWidth"], 128)
            self.assertEqual(record["frameHeight"], 128)
            self.assertEqual(record["source"], "pixellab")
            self.assertEqual(set(record["animations"]), {"idle", "walk", "attack", "hurt", "death"})
            image_path = ROOT / record["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn(key, script)

        self.assertIn("const MONSTER_KIND_SPRITES = {", script)
        self.assertIn("MONSTER_KIND_SPRITES[entity.kind]", script)

    def test_pixellab_monster_frames_are_normalized_inside_sprite_slots(self) -> None:
        manifest_path = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
        monsters = json.loads(manifest_path.read_text(encoding="utf-8"))["monsters"]
        keys = [
            "forest_slime",
            "thorn_boar",
            "moss_imp",
            "wild_mushroom",
            "bark_guard",
            "cave_bat",
            "crystal_lurker",
            "stone_crawler",
            "cloud_wisp",
            "storm_harpy",
            "sun_mote",
            "rust_guard",
            "hollow_knight",
            "cursed_squire",
            "cave_warden",
            "tempest_seraph",
            "throne_keeper",
        ]

        for key in keys:
            record = monsters[key]
            width, _height, pixels = read_png(ROOT / record["image"].lstrip("/"))
            frame_width = record["frameWidth"]
            frame_height = record["frameHeight"]
            min_visible_pixels = 120 if frame_width == 64 else 420
            for animation in ("idle", "walk", "attack"):
                row = record["animations"][animation]["row"]
                for frame in range(record["animations"][animation]["frames"]):
                    frame_pixels = self.frame_pixels(pixels, width, frame_width, frame_height, row, frame)
                    bbox = self.alpha_bbox(frame_pixels, frame_width, frame_height)
                    self.assertIsNotNone(bbox, f"{key} {animation} frame {frame + 1} is empty")
                    assert bbox is not None
                    visible_pixels = sum(
                        1 for index in range(3, len(frame_pixels), 4) if frame_pixels[index] > 8
                    )
                    self.assertGreaterEqual(
                        visible_pixels,
                        min_visible_pixels,
                        f"{key} {animation} frame {frame + 1} is too sparse",
                    )
                    self.assertGreaterEqual(bbox[0], 2, f"{key} {animation} frame {frame + 1} touches left edge")
                    self.assertGreaterEqual(bbox[1], 2, f"{key} {animation} frame {frame + 1} touches top edge")
                    self.assertLessEqual(
                        bbox[2],
                        frame_width - 2,
                        f"{key} {animation} frame {frame + 1} touches right edge",
                    )
                    self.assertLessEqual(
                        bbox[3],
                        frame_height - 2,
                        f"{key} {animation} frame {frame + 1} touches bottom edge",
                    )

    def test_pixellab_monster_body_frames_keep_stable_anchor(self) -> None:
        manifest_path = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
        monsters = json.loads(manifest_path.read_text(encoding="utf-8"))["monsters"]
        keys = [
            "forest_slime",
            "thorn_boar",
            "moss_imp",
            "wild_mushroom",
            "bark_guard",
            "cave_bat",
            "crystal_lurker",
            "stone_crawler",
            "cloud_wisp",
            "storm_harpy",
            "sun_mote",
            "rust_guard",
            "hollow_knight",
            "cursed_squire",
            "cave_warden",
            "tempest_seraph",
            "throne_keeper",
        ]

        for key in keys:
            record = monsters[key]
            width, _height, pixels = read_png(ROOT / record["image"].lstrip("/"))
            frame_width = record["frameWidth"]
            frame_height = record["frameHeight"]
            max_center_span = 10.0 if key == "storm_harpy" else (7.0 if frame_width == 64 else 7.0)
            max_area_ratio = 1.75
            for animation in ("idle", "walk", "attack"):
                row = record["animations"][animation]["row"]
                boxes = []
                areas = []
                for frame in range(record["animations"][animation]["frames"]):
                    frame_pixels = self.frame_pixels(pixels, width, frame_width, frame_height, row, frame)
                    bbox = self.monster_body_anchor_bbox(frame_pixels, frame_width, frame_height)
                    if bbox is None:
                        bbox = self.alpha_bbox(frame_pixels, frame_width, frame_height)
                    self.assertIsNotNone(bbox, f"{key} {animation} frame {frame + 1} is empty")
                    assert bbox is not None
                    boxes.append(bbox)
                    areas.append(sum(1 for index in range(3, len(frame_pixels), 4) if frame_pixels[index] > 8))
                centers_y = [(bbox[1] + bbox[3]) / 2 for bbox in boxes]
                bottoms = [bbox[3] for bbox in boxes]
                self.assertLessEqual(
                    max(centers_y) - min(centers_y),
                    max_center_span,
                    f"{key} {animation} body jumps vertically between frames",
                )
                self.assertLessEqual(
                    max(bottoms) - min(bottoms),
                    2,
                    f"{key} {animation} bottom anchor drifts between frames",
                )
                self.assertLessEqual(
                    max(areas) / max(1, min(areas)),
                    max_area_ratio,
                    f"{key} {animation} visible body area changes too much",
                )

    def test_monster_attack_events_drive_pixel_attack_animation(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("monsterAttackEffects: []", script)
        self.assertIn("seenMonsterAttackEventKeys: new Set()", script)
        self.assertIn("function trackMonsterAttackEffects(events = [], scene = null)", script)
        self.assertIn("event.kind !== 'monster_attack'", script)
        self.assertIn("function recentMonsterAttackEffect(entity)", script)
        self.assertIn("if (recentMonsterAttackEffect(entity)) return 'attack'", script)
        self.assertIn("trackMonsterAttackEffects(snapshot.events || [], snapshot.scene)", script)
        self.assertNotIn("if (entity.role === 'boss') return 'attack'", script)


if __name__ == "__main__":
    unittest.main()
