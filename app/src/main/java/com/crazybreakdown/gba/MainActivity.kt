package com.crazybreakdown.gba
import android.app.Activity
import android.os.Bundle
import android.content.Intent
import android.net.Uri
import android.view.Gravity
import android.view.ViewGroup
import android.widget.*

class MainActivity : Activity() {
    private val games = mutableListOf<Uri>()
    private lateinit var list: LinearLayout
    private lateinit var status: TextView
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = 0xFF10131D.toInt()
        window.navigationBarColor = 0xFF10131D.toInt()
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(22, 28, 22, 18)
            setBackgroundColor(0xFF10131D.toInt())
        }
        root.addView(TextView(this).apply {
            text = "GBA ENHANCED"
            textSize = 25f
            setTextColor(0xFFFFFFFF.toInt())
            gravity = Gravity.CENTER_VERTICAL
        })
        root.addView(TextView(this).apply {
            text = "Sua biblioteca Game Boy Advance"
            textSize = 14f
            setTextColor(0xFF9BA7BC.toInt())
            setPadding(0, 5, 0, 22)
        })
        root.addView(Button(this).apply {
            text = "＋  Adicionar / escanear ROMs"
            setOnClickListener { pickRom() }
        }, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        status = TextView(this).apply {
            text = "Selecione arquivos .gba para adicioná-los à biblioteca."
            setTextColor(0xFFB9C4D8.toInt())
            setPadding(0, 18, 0, 12)
        }
        root.addView(status)
        list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        root.addView(list)
        root.addView(TextView(this).apply {
            text = "GRÁFICOS"
            textSize = 12f
            setTextColor(0xFF75D6C2.toInt())
            setPadding(0, 24, 0, 8)
        })
        addToggle(root, "Filtro de imagem / nitidez")
        addToggle(root, "Efeito de profundidade 3D (experimental)")
        addToggle(root, "Sombras (experimental)")
        addToggle(root, "Modo widescreen (por jogo)")
        root.addView(TextView(this).apply {
            text = "Versão inicial: biblioteca e interface. A execução real de ROMs, reconstrução 3D, sombras e patches widescreen dependem da integração dos núcleos e perfis compatíveis."
            textSize = 12f
            setTextColor(0xFF8995AA.toInt())
            setPadding(0, 20, 0, 0)
        })
        setContentView(ScrollView(this).apply { addView(root) })
    }
    private fun addToggle(parent: LinearLayout, label: String) {
        parent.addView(Switch(this).apply {
            text = label
            isChecked = false
            setTextColor(0xFFE7ECF5.toInt())
            textSize = 14f
            isEnabled = false
            alpha = 0.65f
        })
    }
    private fun pickRom() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "*/*"
            putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        }
        startActivityForResult(intent, 41)
    }
    @Deprecated("Deprecated in Android API; retained for compatibility")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != 41 || resultCode != RESULT_OK || data == null) return
        val picked = mutableListOf<Uri>()
        data.clipData?.let { clip -> for (i in 0 until clip.itemCount) picked.add(clip.getItemAt(i).uri) }
        data.data?.let { picked.add(it) }
        picked.forEach { uri ->
            runCatching { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) }
            if (games.none { it == uri }) games.add(uri)
        }
        list.removeAllViews()
        games.forEachIndexed { index, uri ->
            list.addView(TextView(this).apply {
                text = "🎮  " + (index + 1) + ". " + (uri.lastPathSegment ?: "ROM GBA")
                textSize = 14f
                setTextColor(0xFFFFFFFF.toInt())
                setPadding(10, 12, 10, 12)
            })
        }
        status.text = games.size.toString() + " arquivo(s) selecionado(s)."
    }
}
