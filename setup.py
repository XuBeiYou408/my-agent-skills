import os
import sys
import shutil
import json
from pathlib import Path

def setup():
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("🚀 正在为您自动安装并配置 幼麟的专属 Agent 技能库与全局人设...")
    
    user_home = Path.home()
    current_dir = Path(__file__).parent.resolve()
    
    # 1. 部署全局人设 (Global Persona / Rules)
    persona_src = current_dir / "GEMINI.md"
    if persona_src.exists():
        persona_dests = [
            user_home / ".gemini" / "antigravity" / "scratch" / "GEMINI.md",
            user_home / ".gemini" / "GEMINI.md"
        ]
        for dest in persona_dests:
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(persona_src, dest)
                print(f"  ✨ 已成功部署全局人设规范: -> {dest}")
            except Exception as e:
                print(f"  ⚠️ 部署全局人设到 {dest} 失败: {e}")

    # 2. 部署技能库 (Skills)
    global_skills_dir = user_home / ".gemini" / "config" / "skills"
    global_skills_dir.mkdir(parents=True, exist_ok=True)
    
    source_skills_dir = current_dir / "skills"
    if not source_skills_dir.exists():
        print("❌ 未能找到 skills 目录！")
        sys.exit(1)
        
    manifest_file = current_dir / "SKILL_MANIFEST.json"
    skills_to_install = []
    
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                skills_to_install = [s["name"] for s in manifest.get("skills", [])]
        except Exception:
            skills_to_install = [d.name for d in source_skills_dir.iterdir() if d.is_dir()]
    else:
        skills_to_install = [d.name for d in source_skills_dir.iterdir() if d.is_dir()]
        
    installed_count = 0
    for skill_name in skills_to_install:
        src = source_skills_dir / skill_name
        dest = global_skills_dir / skill_name
        
        if src.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f"  ✅ 已成功挂载 Skill: {skill_name} -> {dest}")
            installed_count += 1
            
    print(f"\n🎉 全部完成！已为您成功装载 {installed_count} 个 Skill 以及全局人设规范到系统配置中。")
    print("现在所有的 Agent (Antigravity, Gemini, Kimi, Claude Code 等) 均已支持并可直接调用！")

if __name__ == "__main__":
    setup()
