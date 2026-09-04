from __future__ import annotations


DEMO_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>老年人跌倒风险监测演示</title>
  <style>
    :root{font-family:Inter,"Microsoft YaHei",sans-serif;color:#e8eef7;background:#0b1220}
    *{box-sizing:border-box} body{margin:0;background:linear-gradient(145deg,#09111f,#111c30);min-height:100vh}
    header{padding:22px 28px;border-bottom:1px solid #26344c;background:#0d1728}
    h1{font-size:23px;margin:0 0 6px} .sub{color:#8fa2be;font-size:13px}
    main{display:grid;grid-template-columns:minmax(520px,1.7fr) minmax(330px,1fr);gap:18px;padding:18px;max-width:1500px;margin:auto}
    .card{background:#111d30;border:1px solid #263751;border-radius:14px;padding:16px;box-shadow:0 12px 30px #0004}
    .controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:14px}
    label{font-size:12px;color:#a9b8cc} select,input,button{width:100%;margin-top:5px;padding:10px;border-radius:8px;border:1px solid #344863;background:#0c1626;color:#eef5ff}
    button{cursor:pointer;font-weight:700;background:#2672e7;border-color:#3884f5} button.stop{background:#732d3d;border-color:#a8455b}
    .video{aspect-ratio:16/9;background:#05080e;border-radius:10px;display:flex;align-items:center;justify-content:center;overflow:hidden;color:#66758b}
    .video img{width:100%;height:100%;object-fit:contain}.actions{display:flex;gap:10px;margin-top:10px}
    .risk{font-size:36px;font-weight:800;margin:4px 0 14px;color:#8796aa}.risk.NORMAL{color:#42d487}.risk.LOW{color:#f3cf58}.risk.MEDIUM{color:#f49a46}.risk.HIGH,.risk.FALL_CONFIRMED{color:#ff596d}
    .prob{margin:12px 0}.prob-head{display:flex;justify-content:space-between;font-size:13px}.bar{height:9px;background:#23324a;border-radius:8px;margin-top:6px;overflow:hidden}.fill{height:100%;width:0;background:#4b91ff;transition:width .3s}
    .kv{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:16px}.metric{padding:10px;background:#0d1727;border-radius:9px}.metric b{display:block;font-size:18px;margin-top:4px}.metric span{font-size:11px;color:#90a4bf}
    .notice{font-size:12px;color:#9eb0c7;line-height:1.7;margin-top:13px;padding:10px;border-left:3px solid #3e78ca;background:#0d1727}
    #message{font-size:12px;min-height:18px;color:#f3cf58;margin-top:8px;word-break:break-all}
    @media(max-width:900px){main{grid-template-columns:1fr}.controls{grid-template-columns:1fr}}
  </style>
</head>
<body>
<header><h1>老年人跌倒风险监测演示</h1><div class="sub">实时跌倒检测 + 未来 1 / 2 / 3 秒风险预测</div></header>
<main>
  <section class="card">
    <div class="controls">
      <label>视频来源<select id="sourceType"><option value="demo">内置成功样例</option><option value="ezviz">萤石摄像头</option><option value="direct">直接流地址</option></select></label>
      <label>服务 API Key（未配置可留空）<input id="apiKey" type="password" placeholder="FALL_SERVICE_API_KEY"></label>
      <label id="deviceWrap">设备序列号<input id="deviceSerial" placeholder="萤石设备序列号"></label>
      <label id="urlWrap">视频/RTSP/RTMP 地址<input id="sourceUrl" placeholder="rtsp://... 或本地视频绝对路径"></label>
    </div>
    <div class="video"><span id="placeholder">点击“开始处理”后显示画面</span><img id="frame" alt="实时处理画面" hidden></div>
    <div class="actions"><button id="start">开始处理</button><button class="stop" id="stop">停止</button></div>
    <div id="message"></div>
  </section>
  <aside class="card">
    <div class="sub">当前预测状态</div><div id="risk" class="risk">未启动</div>
    <div class="prob"><div class="prob-head"><span>1 秒内风险</span><b id="p1Text">--</b></div><div class="bar"><div class="fill" id="p1"></div></div></div>
    <div class="prob"><div class="prob-head"><span>2 秒内风险</span><b id="p2Text">--</b></div><div class="bar"><div class="fill" id="p2"></div></div></div>
    <div class="prob"><div class="prob-head"><span>3 秒内风险</span><b id="p3Text">--</b></div><div class="bar"><div class="fill" id="p3"></div></div></div>
    <div class="kv">
      <div class="metric"><span>跌倒检测状态</span><b id="fallState">--</b></div>
      <div class="metric"><span>跌倒概率</span><b id="fallProb">--</b></div>
      <div class="metric"><span>骨架有效率</span><b id="poseRatio">--</b></div>
      <div class="metric"><span>已处理帧数</span><b id="frames">0</b></div>
    </div>
    <div class="notice" style="margin-top:16px;border-left-color:#a56be8">
      <b>Qwen3-VL 多模态复核</b><br>
      状态：<span id="mmStatus">--</span>　动作：<span id="mmAction">--</span>　风险：<span id="mmRisk">--</span><br>
      融合建议：<span id="mmFusion">--</span><br>
      <span id="mmSummary">疑似风险出现后异步分析最近的RGB视频片段。</span><br>
      <span id="mmEvidence"></span>
    </div>
    <div class="notice">LOW / MEDIUM / HIGH 分别表示预测 3 / 2 / 1 秒内存在风险。POSE_UNAVAILABLE 表示当前骨架质量不足，不能当作“正常”。当前预测模块用于提示和人工复核。</div>
  </aside>
</main>
<script>
const $=id=>document.getElementById(id); let timer=null,frameTimer=null,lastFrameUrl=null;
function headers(){const h={'Content-Type':'application/json'},k=$('apiKey').value.trim();if(k)h['X-API-Key']=k;return h}
function showInputs(){const t=$('sourceType').value;$('deviceWrap').style.display=t==='ezviz'?'block':'none';$('urlWrap').style.display=t==='direct'?'block':'none'}
$('sourceType').onchange=showInputs;showInputs();
async function call(path,opts={}){const r=await fetch(path,{...opts,headers:{...headers(),...(opts.headers||{})}});const body=await r.json().catch(()=>({}));if(!r.ok)throw new Error(body.detail||r.statusText);return body}
function fmt(v){return typeof v==='number'?(v*100).toFixed(1)+'%':'--'}
function setProb(id,v){$(id).style.width=(typeof v==='number'?Math.max(0,Math.min(100,v*100)):0)+'%';$(id+'Text').textContent=fmt(v)}
function render(s){const latest=s.latest_result||{},p=latest.prefall_prediction||{},m=latest.multimodal_review||s.multimodal_review||{},risk=p.risk_level||(s.running?'WARMUP':'未启动');$('risk').textContent=risk;$('risk').className='risk '+risk;setProb('p1',p.probabilities?.['1s']);setProb('p2',p.probabilities?.['2s']);setProb('p3',p.probabilities?.['3s']);$('fallState').textContent=latest.state||s.state||'--';$('fallProb').textContent=fmt(latest.fall_probability);$('poseRatio').textContent=fmt(latest.pose_valid_ratio);$('frames').textContent=s.frames_processed||0;$('mmStatus').textContent=m.status||'--';$('mmAction').textContent=m.action_class||'--';$('mmRisk').textContent=m.risk_level||'--';$('mmFusion').textContent=m.fusion_decision||'--';$('mmSummary').textContent=m.summary_zh||'疑似风险出现后异步分析最近的RGB视频片段。';$('mmEvidence').textContent=m.evidence?('依据：'+m.evidence):'';if(s.last_error)$('message').textContent=s.last_error;if(m.error)$('message').textContent='多模态复核：'+m.error}
async function poll(){try{render(await call('/v1/streams/status'))}catch(e){$('message').textContent=e.message}}
async function refreshFrame(){try{const r=await fetch('/v1/frame.jpg',{headers:headers()});if(!r.ok)return;const u=URL.createObjectURL(await r.blob());$('frame').src=u;$('frame').hidden=false;$('placeholder').hidden=true;if(lastFrameUrl)URL.revokeObjectURL(lastFrameUrl);lastFrameUrl=u}catch(e){}}
$('start').onclick=async()=>{try{const t=$('sourceType').value,b={source_type:t,process_every_n_frames:1};if(t==='ezviz')b.device_serial=$('deviceSerial').value.trim()||null;if(t==='direct')b.source_url=$('sourceUrl').value.trim();$('message').textContent='正在启动并加载模型，请稍候……';await call('/v1/streams/start',{method:'POST',body:JSON.stringify(b)});$('message').textContent='已启动；积累满 64 帧后开始预测。';clearInterval(timer);clearInterval(frameTimer);timer=setInterval(poll,1000);frameTimer=setInterval(refreshFrame,500);poll()}catch(e){$('message').textContent='启动失败：'+e.message}}
$('stop').onclick=async()=>{try{await call('/v1/streams/stop',{method:'POST'});$('message').textContent='已停止';clearInterval(timer);clearInterval(frameTimer);poll()}catch(e){$('message').textContent=e.message}}
poll();
</script>
</body></html>'''
