var catan_add_loading_scene = function(game, left, top, width, info_height) {
    // 加载所有声音和图片sprites
    // https://craftyjs.com/api/Crafty-audio.html#Crafty-audio-play
    game.load_assets = function() {
        const loading_text_h = info_height;
        const loading_bar_h = info_height;
        const loading_color = "#006600"
        console.log("LOADING: Crafty.support.audio = " + Crafty.support.audio);
        var loading_text = Crafty.e("2D, DOM, Text")
            .attr({
                x: left,
                y: top,
                w: width,
                h: loading_text_h,
            })
            .text("加载中...")
            .css({ "text-align": "center" })
            .textColor(loading_color)
            .textFont({ type: 'italic', family: 'Arial', size: `${loading_text_h * 0.6}px`, weight: 'bold'});

        Crafty.e("2D, DOM, ProgressBar")
            .attr({
                x: left,
                y: top + loading_text_h,
                w: width,
                h: loading_bar_h,
                z: 100
            })
            // progressBar(Number maxValue, Boolean flipDirection, String emptyColor, String filledColor)
            .progressBar(100, false, "grey", loading_color)
            .bind("LOADING_PROGRESS", function(percent) {
                // updateBarProgress(Number currentValue)
                this.updateBarProgress(percent);
            });

        var loaded = function() {
            Crafty.scene("main");
            // 部分浏览器无法加载Audio，所以单独列出加载
            Crafty.load(audio_asserts, function(){
                console.log("LOADING: audios loaded");
            });
        }
        var progress = function(e) {
            // console.log("loading");
            const pct = Math.floor(e.percent);
            var text;
            if (pct >= 100) {
                text = "加载完毕";
            }
            else if (pct >= 80) {
                text = "展开贸易";
            }
            else if (pct >= 60) {
                text = "修建设施";
            }
            else if (pct >= 40) {
                text = "居民入住";
            }
            else if (pct >= 20) {
                text = "填充陆地";
            }
            else {
                text = "开拓海洋"
            }
            loading_text.text(`${pct}%: ${text}...`)
            Crafty.trigger("LOADING_PROGRESS", e.percent);
        };
        var error_loading = function(e) {
            console.log("loading error"); console.log(e);
        };
        Crafty.load(assets, loaded, progress, error_loading);
    }
    return game;
}
