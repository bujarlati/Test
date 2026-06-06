from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WebStaticTests(unittest.TestCase):
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
            "equipmentSlotList",
            "newCharacterButton",
        ):
            self.assertIn(marker, html)

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
        self.assertIn("advanceVisualState", script)
        self.assertIn("applyCameraDamping", script)
        self.assertIn("drawBlendedSpriteBottom", script)
        self.assertIn("return (x - cameraX) * worldScale + 56", script)

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
        self.assertIn("skeleton.head.y - 24", script)

    def test_frontend_renders_exp_revive_and_equipment_slots(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("expText", script)
        self.assertIn("expProgressBar", script)
        self.assertIn("reviveText", script)
        self.assertIn("renderEquipmentSlots", script)
        self.assertIn("equipment_slots", script)
        self.assertIn("reviving", script)
        self.assertIn("复活中", script)

    def test_frontend_draws_equipped_models_and_item_previews(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        for marker in (
            "equipmentAppearance(",
            "equipmentPreviewHtml",
            "drawEquippedArmor",
            "drawEquippedHelmet",
            "drawEquippedBoots",
            "drawEquippedRing",
            "drawEquipmentGlow",
            "drawWeaponOnHand(skeleton.mainHand, equipped.weapon",
        ):
            self.assertIn(marker, script)

        self.assertIn("equipmentPreviewHtml(item)", script)
        self.assertIn("gear-preview", styles)
        self.assertIn("gear-core", styles)
        self.assertIn("gear-edge", styles)

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

    def test_frontend_persists_local_character(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("idleForestProfile", script)
        self.assertIn("/profile/roll", script)
        self.assertIn("/profile/confirm", script)


if __name__ == "__main__":
    unittest.main()
