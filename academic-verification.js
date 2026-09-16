(() => {
  const style = document.createElement('style');
  style.textContent = `.dg-verification-legend{margin:12px 0;padding:12px 14px;border:1px solid #e3e8e3;border-radius:12px;background:#fff;font-size:.88rem}.dg-verification-legend strong{color:#1b4332}.dg-verification-items{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.dg-verification-item{padding:5px 9px;border-radius:999px;background:#f5f8f4}.dg-status-verified{border-left:4px solid #2d6a4f}.dg-status-review{border-left:4px solid #d4a373}.dg-status-modern{border-left:4px solid #457b9d}.dg-status-draft{border-left:4px solid #8b8b8b}`;
  document.head.appendChild(style);
  const addLegend = () => {
    if (document.querySelector('.dg-verification-legend')) return true;
    const host = document.querySelector('.plant-hero') || document.querySelector('main');
    if (!host) return false;
    const legend = document.createElement('div');
    legend.className = 'dg-verification-legend';
    legend.setAttribute('role','note');
    legend.innerHTML = '<strong>Academic verification status</strong><div class="dg-verification-items"><span class="dg-verification-item dg-status-verified">🟢 Classically verified</span><span class="dg-verification-item dg-status-review">🟡 Needs text-level verification</span><span class="dg-verification-item dg-status-modern">🔵 Modern reference</span><span class="dg-verification-item dg-status-draft">⚪ Working draft</span></div><div style="margin-top:7px;color:#6b756f">Educational reference. Check authoritative Ayurvedic texts and professional guidance before clinical use.</div>';
    host.insertAdjacentElement('afterend', legend);
    return true;
  };
  if (!addLegend()) new MutationObserver((_, obs) => { if (addLegend()) obs.disconnect(); }).observe(document.body, {childList:true,subtree:true});
})();
