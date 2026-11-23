#!/usr/bin/env python3
"""Apply the GBA Enhanced Android customizations to the pinned SkyEmu checkout."""
from pathlib import Path

root = Path("vendor/SkyEmu")
activity = root / "tools/android_project/app/src/main/java/com/sky/SkyEmu/EnhancedNativeActivity.java"
source = activity.read_text(encoding="utf-8")

source = source.replace(
    "import java.util.Vector;\n",
    "import java.util.Vector;\nimport java.util.zip.ZipEntry;\nimport java.util.zip.ZipInputStream;\n"
)
source = source.replace(
    "return metrics.xdpi/120.0f;",
    "// Use Android's logical density and a compact multiplier instead of physical xdpi.\n        return metrics.density * 0.80f;"
)
source = source.replace(
    "return Locale.getDefault().toString();",
    "// SkyEmu's locale parser expects the language code without the region (e.g. pt, not pt_BR).\n        return Locale.getDefault().getLanguage();"
)

old = """    public void loadURI(Uri selectedFileUri, boolean is_rom){
        String filename = getFileName(selectedFileUri);
        File file = new File(selectedFileUri.getPath());//create path from uri
        Log.i("SkyEmu", "Selected file path: " + filename);

        if (selectedFileUri != null) {
            // Get the original file's path using its URI
            // Copy the file to the external directory
            String externalDirectoryPath = getExternalFilesDir(null).getAbsolutePath();
            File copiedFile = copyFileToExternalDirectory(selectedFileUri, externalDirectoryPath,filename);

            if (copiedFile != null) {
                String copiedFilePath = copiedFile.getAbsolutePath();
                if(is_rom)se_android_load_rom(copiedFilePath);
                se_android_load_file(copiedFilePath);
                Log.i("SkyEmu", "Copied file path: " + copiedFilePath);
            }
        }
    }"""

new = """    private boolean isSupportedRom(String name) {
        String lower = name.toLowerCase(Locale.ROOT);
        return lower.endsWith(".gba") || lower.endsWith(".gbc") ||
                lower.endsWith(".gb") || lower.endsWith(".nds");
    }

    // Extract only a supported ROM entry; never trust archive paths and cap output size.
    private File extractRomFromZip(File archive) {
        final long maxRomBytes = 64L * 1024L * 1024L;
        File outputDirectory = getExternalFilesDir(null);
        if (outputDirectory == null) return null;
        try (ZipInputStream zip = new ZipInputStream(new java.io.BufferedInputStream(
                new java.io.FileInputStream(archive)))) {
            ZipEntry entry;
            while ((entry = zip.getNextEntry()) != null) {
                if (entry.isDirectory() || !isSupportedRom(entry.getName())) continue;
                String safeName = new File(entry.getName()).getName();
                if (safeName.isEmpty()) continue;
                File output = new File(outputDirectory, "rom_" + System.currentTimeMillis() + "_" + safeName);
                long total = 0;
                try (OutputStream out = new FileOutputStream(output)) {
                    byte[] buffer = new byte[8192];
                    int count;
                    while ((count = zip.read(buffer)) != -1) {
                        total += count;
                        if (total > maxRomBytes) {
                            out.close();
                            output.delete();
                            return null;
                        }
                        out.write(buffer, 0, count);
                    }
                }
                if (total > 0) return output;
                output.delete();
            }
        } catch (IOException error) {
            Log.e(TAG, "Could not extract ROM from ZIP", error);
        }
        return null;
    }

    public void loadURI(Uri selectedFileUri, boolean is_rom){
        if (selectedFileUri == null) return;
        String filename = getFileName(selectedFileUri);
        Log.i("SkyEmu", "Selected file: " + filename);
        String externalDirectoryPath = getExternalFilesDir(null).getAbsolutePath();
        File copiedFile = copyFileToExternalDirectory(selectedFileUri, externalDirectoryPath, filename);
        if (copiedFile == null) {
            android.widget.Toast.makeText(this, "Não foi possível abrir o arquivo", android.widget.Toast.LENGTH_LONG).show();
            return;
        }

        File gameFile = copiedFile;
        if (filename.toLowerCase(Locale.ROOT).endsWith(".zip")) {
            gameFile = extractRomFromZip(copiedFile);
            if (gameFile == null) {
                android.widget.Toast.makeText(this, "O ZIP não contém uma ROM compatível (.gba, .gbc, .gb ou .nds)", android.widget.Toast.LENGTH_LONG).show();
                return;
            }
        }

        String gamePath = gameFile.getAbsolutePath();
        boolean isRomFile = is_rom || isSupportedRom(gameFile.getName());
        if (isRomFile) se_android_load_rom(gamePath);
        se_android_load_file(gamePath);
        Log.i(TAG, "Loading game file: " + gamePath);
    }"""

if old not in source:
    raise SystemExit("Could not locate loadURI implementation; refusing to patch the wrong source.")
source = source.replace(old, new)
activity.write_text(source, encoding="utf-8")

localization = root / "src/localization.c"
c = localization.read_text(encoding="utf-8")
marker = "char ** localization_map=NULL;"
if "pt_localization_array" not in c:
    portuguese = r'''
// Brazilian Portuguese translations for the Android build.
static char* pt_localization_array[]={
    "Open ROM", "Abrir ROM",
    "Load Game", "Carregar jogo",
    "Load ROM from file (%s)", "Carregar ROM de um arquivo (%s)",
    "You can also drag & drop a ROM to load it", "Você também pode arrastar uma ROM para carregá-la",
    "Load ROM(%s), save(.sav), or GBA bios (gba_bios.bin) from file", "Carregar ROM (%s), salvamento (.sav) ou BIOS do GBA (gba_bios.bin)",
    "You can also drag & drop a ROM/save file to load it", "Você também pode arrastar uma ROM ou arquivo de salvamento",
    "Load Recently Played Game", "Carregar jogo recente",
    "No recently played games", "Nenhum jogo recente",
    "Controllers", "Controles",
    "Controller", "Controle",
    "No Controller", "Nenhum controle",
    "Reset Default Controller Bindings", "Restaurar configuração padrão dos controles",
    "Save States", "Estados de salvamento",
    "Save Slot %d", "Slot de salvamento %d",
    "Capture", "Salvar",
    "Restore", "Carregar",
    "Display Settings", "Configurações de vídeo",
    "Screen Shader", "Filtro de imagem",
    "Pixelate", "Pixelado",
    "Bilinear", "Bilinear",
    "Screen Rotation", "Rotação da tela",
    "Color Correction", "Correção de cores",
    "Strength: %.2f", "Intensidade: %.2f",
    "Screen Ghosting", "Rastro da tela",
    "Force Integer Scaling", "Forçar escala inteira",
    "Stretch Screen to Fit", "Ajustar tela para preencher",
    "Game Boy Color Palette", "Paleta do Game Boy Color",
    "Reset Palette to Defaults", "Restaurar paleta padrão",
    "Keybinds", "Atalhos do teclado",
    "Reset Default Keybinds", "Restaurar atalhos padrão",
    "Advanced", "Avançado",
    "Light Mode", "Modo claro",
    "Dark", "Escuro",
    "Light", "Claro",
    "Show Debug Tools", "Mostrar ferramentas de depuração",
    "Adjust volume", "Ajustar volume",
    "Show/Hide Menu Panel", "Mostrar/ocultar painel do menu",
    "Screen", "Tela",
    "Menu", "Menu",
    "Current", "Atual",
    "Original", "Original",
    "Opacity", "Opacidade",
    "Touch Control Settings", "Configurações dos controles de toque",
    "Hide when inactive", "Ocultar quando inativo",
    "Open File From Disk", "Abrir arquivo do dispositivo",
    "Exit File Browser", "Sair do navegador de arquivos",
    "Go back to recently loaded games", "Voltar aos jogos recentes",
    "Go to parent directory", "Voltar à pasta anterior",
    "Reset Game", "Reiniciar jogo",
    "Theme", "Tema",
    "Brightness: %.2f", "Brilho: %.2f",
    "Always Show Menu/Nav Bar", "Sempre mostrar barras de menu e navegação",
    "Language", "Idioma",
    "Scale", "Escala",
    "Scale: %.2f", "Escala: %.2f",
    "Full Screen", "Tela cheia",
    "Save File/State Path", "Pasta de salvamentos",
    "BIOS/Firmware Path", "Pasta da BIOS/firmware",
    "Create new save files in Save Path", "Criar novos salvamentos na pasta definida",
    "Force GB games to run in DMG mode", "Forçar jogos de GB no modo DMG",
    "Server Port", "Porta do servidor",
    "Toggle Full Screen", "Alternar tela cheia",
    "Audio", "Áudio",
    "Left Audio Channel", "Canal de áudio esquerdo",
    "Right Audio Channel", "Canal de áudio direito",
    "Build Info", "Informações da versão",
    "Export Save", "Exportar salvamento",
    "Save File", "Arquivo de salvamento",
    "Rewind", "Retroceder",
    "Fast Forward", "Avanço rápido",
    "Pause", "Pausar",
    "Resume", "Continuar",
    "Cancel", "Cancelar",
    "Yes", "Sim",
    "No", "Não",
    "Enabled", "Ativado",
    "Disabled", "Desativado",
    "Default", "Padrão",
    "Apply", "Aplicar",
    "Settings", "Configurações",
    "Options", "Opções",
    "Back", "Voltar",
    "Close", "Fechar",
    "On", "Ligado",
    "Off", "Desligado",
    "Never", "Nunca",
    "Always", "Sempre",
    "Automatic", "Automático",
    "Language", "Idioma",
    NULL,NULL
};
'''
    if marker not in c:
        raise SystemExit("Could not locate localization map insertion point.")
    c = c.replace(marker, portuguese + "\n" + marker)
    c = c.replace(
        "if(language_enum==SE_LANG_JAPANESE)new_map = ja_localization_array;",
        "if(language_enum==SE_LANG_JAPANESE)new_map = ja_localization_array;\n    if(language_enum==SE_LANG_PORTUGESE)new_map = pt_localization_array;"
    )
    localization.write_text(c, encoding="utf-8")

print("Applied compact Android UI, Portuguese UI translations, and ZIP ROM loading.")
