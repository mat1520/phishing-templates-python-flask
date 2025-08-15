#!/usr/bin/env python3
"""
Script para verificar sitios que pueden tener problemas de CSS/JS
"""
import os

SITES_DIR = 'sites'

def check_site_files(site_name):
    """Verifica archivos importantes en un sitio"""
    site_path = os.path.join(SITES_DIR, site_name)
    if not os.path.exists(site_path):
        return f"❌ {site_name}: No existe"
    
    files = []
    for root, dirs, file_list in os.walk(site_path):
        for file in file_list:
            rel_path = os.path.relpath(os.path.join(root, file), site_path)
            files.append(rel_path)
    
    print(f"\n🔍 {site_name.upper()}")
    print(f"📁 Archivos encontrados: {len(files)}")
    
    # Buscar archivos CSS y JS
    css_files = [f for f in files if f.endswith('.css')]
    js_files = [f for f in files if f.endswith('.js')]
    
    if css_files:
        print(f"🎨 CSS: {len(css_files)} archivos")
        for css in css_files[:3]:  # Mostrar solo los primeros 3
            print(f"   - {css}")
    else:
        print("⚠️  No se encontraron archivos CSS")
    
    if js_files:
        print(f"⚡ JS: {len(js_files)} archivos")
        for js in js_files[:3]:  # Mostrar solo los primeros 3
            print(f"   - {js}")
    else:
        print("⚠️  No se encontraron archivos JS")
    
    # Verificar index files
    index_files = [f for f in files if 'index' in f.lower()]
    if index_files:
        print(f"🏠 Index files: {', '.join(index_files)}")

def main():
    print("🔍 VERIFICADOR DE SITIOS - PROBLEMAS DE CSS/JS")
    print("=" * 50)
    
    # Sitios que pueden tener problemas
    problematic_sites = [
        'netflix', 'instagram', 'facebook', 'google', 'github',
        'microsoft', 'protonmail', 'steam', 'spotify'
    ]
    
    for site in problematic_sites:
        check_site_files(site)
    
    print(f"\n✅ Verificación completada")
    print(f"💡 Tip: Los sitios sin CSS/JS pueden tener problemas de diseño")

if __name__ == "__main__":
    main()
