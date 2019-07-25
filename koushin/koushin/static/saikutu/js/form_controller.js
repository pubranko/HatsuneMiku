//s = searchの略
var sch_count = 0;      //サーチ数の初期値
var grp_count = 1;      //グループ数の初期値
var xhr_request;        //ajaxによるリクエスト保存エリア
var page_count = 1;     //ページ数。初期値は1頁目。

/**初回の読み込み時に、入力フォームの1つ目を追加 。
 * ただし検索結果を別のタブで開く場合は操作なし。
*/
window.onload = function(){

    if (document.getElementsByClassName('cls_s').length == 1){
        // ページ読み込み時に実行したい処理
        f_input_form_add(document,0);
    }
}

/**入力フォームを追加する関数。
 * 同時に追加用のボタンを下に追加する。
 */
function f_input_form_add(mydocument,sch_num){
    sch_count += 1;
    let i = 0;
    /*タグの階層関係
    <div>
        <select>
            <option>
            〜
        <input> ※textフィールド
        <input> ※チェックボックス
        not
        <input> ※条件削除ボタン
        <input> ※条件追加ボタン
    */

    //divタグを作成し、条件フィールドと条件追加ボタンを中に設定する。
    let div_tag = document.createElement('div'); 
    div_tag.className='cls_s cls_grp_elem cls_s'+sch_count;
    //selectタグを作成。またその中にoptionタグを追加していく。
    let select_tag = document.createElement('select');
    select_tag.name = 'Filed';
    let option_tag_0 = document.createElement('option');
    option_tag_0.value = '0';
    option_tag_0.selected = true;
    option_tag_0.innerHTML ='件名or本文';
    option_tag_0.setAttribute('onclick', 'f_input_form_change(document,'+sch_count+',0)');
    select_tag.appendChild(option_tag_0);
    let option_tag_1 = document.createElement('option');
    option_tag_1.value = '1';
    option_tag_1.innerHTML ='件名';
    option_tag_1.setAttribute('onclick', 'f_input_form_change(document,'+sch_count+',1)');
    select_tag.appendChild(option_tag_1);
    let option_tag_2 = document.createElement('option');
    option_tag_2.value = '2';
    option_tag_2.innerHTML ='本文';
    option_tag_2.setAttribute('onclick', 'f_input_form_change(document,'+sch_count+',2)');
    select_tag.appendChild(option_tag_2);
    let option_tag_3 = document.createElement('option');
    option_tag_3.value = '3';
    option_tag_3.innerHTML ='記事公開日';
    option_tag_3.setAttribute('onclick', 'f_input_form_change(document,'+sch_count+',3)');
    select_tag.appendChild(option_tag_3);
    let option_tag_4 = document.createElement('option');
    option_tag_4.value = '4';
    option_tag_4.innerHTML ='発行者';
    option_tag_4.setAttribute('onclick', 'f_input_form_change(document,'+sch_count+',4)');
    select_tag.appendChild(option_tag_4);
    
    //最後にselectタグをdivタグへ追加
    div_tag.appendChild(select_tag);
    //項目間の空白調整
    let brank_area = document.createTextNode(' ');
    div_tag.appendChild(brank_area);

    //inputタグ（検索条件入力フィールド）を作成し、divタグへ追加
    let input_tag_text = document.createElement('input');
    input_tag_text.type = 'text';
    input_tag_text.className = 'sch_field_'+sch_count;
    input_tag_text.name = 'sch_text_'+sch_count;
    input_tag_text.value = '';
    div_tag.appendChild(input_tag_text);

    brank_area = document.createTextNode(' ');
    div_tag.appendChild(brank_area);

    //inputタグ（チェックボックス）を作成し、divタグへ追加
    let input_tag_checkbox = document.createElement('input');
    input_tag_checkbox.type = 'checkbox';
    input_tag_checkbox.name = 'search_option_not_'+sch_count;
    input_tag_checkbox.value = 'not_search';
    div_tag.appendChild(input_tag_checkbox);
    let not_tag = document.createTextNode('not(まだ未実装) ');
    div_tag.appendChild(not_tag);

    //inputタグ（条件削除ボタン）を作成し、divタグへ追加
    let input_tag_button_del = document.createElement('input');
    input_tag_button_del.type = 'button';
    input_tag_button_del.value = '条件削除';
    input_tag_button_del.className = 'cls_button_control1';
    input_tag_button_del.setAttribute('onclick', 'f_input_search_delete(document,'+sch_count+')');
    div_tag.appendChild(input_tag_button_del);

    brank_area = document.createTextNode(' ');
    div_tag.appendChild(brank_area);

    //inputタグ（条件追加ボタン）を作成し、divタグへ追加
    let input_tag_button_add = document.createElement('input');
    input_tag_button_add.type = 'button';
    input_tag_button_add.value = '条件追加↓';
    input_tag_button_add.name = 'sch_add'+sch_count;
    input_tag_button_add.className = 'cls_button_control1';
    input_tag_button_add.setAttribute('onclick', 'f_input_form_add(document,'+sch_count+')');
    div_tag.appendChild(input_tag_button_add);

    //押下された条件追加ボタンを取得し、その次に新なフィールド(divタグ)を追加。
    let elem = mydocument.getElementsByClassName("cls_s"+sch_num);
    elem[0].parentNode.insertBefore(div_tag, elem[0].nextSibling); 
}

/**入力フォームを削除する。同時に下にある追加用ボタンを削除する。
 */
function f_input_search_delete(mydocument,sch_num){
    let get_div = mydocument.getElementsByClassName("cls_s"+sch_num);
    get_div[0].parentNode.removeChild(get_div[0]);
}
/**検索フィールドを、テキスト（タイトル・本文・発行者）、日付（公開日）の切り替える
 * 引数（ドキュメント、条件の番号、選択されたオプションのvalue）
 */
function f_input_form_change(mydocument,sch_num,op_val){
    //検索フィールドの要素をリストで取得
    let get_div = mydocument.getElementsByClassName('cls_grp_elem');
    //チェンジ前の検索フィールドがtextかdateか判定するため、対象のフィールドを取得
    let get_sch_field = mydocument.getElementsByClassName('sch_field_'+sch_num);

    //textとdateが変る場合、検索フィールドを切り替え
    if(op_val == 3 && get_sch_field[0].type == 'text'){
        //テキスト→日付フィールドへチェンジ
        let input_date_from = document.createElement('input');
        input_date_from.type = 'date';
        input_date_from.name = 'sch_date_from_'+sch_num;
        input_date_from.className = get_sch_field[0].className;
        input_date_from.value = '';
        let input_date_to = document.createElement('input');
        input_date_to.type = 'date';
        input_date_to.name = 'sch_date_to_'+sch_num;
        input_date_to.className = get_sch_field[0].className;
        input_date_to.value = '';
        get_sch_field[0].parentNode.insertBefore(input_date_to, get_sch_field[0].nextSibling); 
        get_sch_field[0].parentNode.insertBefore(input_date_from, get_sch_field[0].nextSibling); 
        get_sch_field[0].parentNode.removeChild(get_sch_field[0]);  //sch_textを削除
    }else if(op_val != 3 && get_sch_field[0].type == 'date'){
        //日付→テキストフィールドへチェンジ
        let input_tag_text = document.createElement('input');
        input_tag_text.type = 'text';
        input_tag_text.name = 'sch_text_'+sch_num;
        input_tag_text.className = get_sch_field[0].className;
        input_tag_text.value = '';
        get_sch_field[0].parentNode.insertBefore(input_tag_text, get_sch_field[0].nextSibling); 
        get_sch_field[0].parentNode.removeChild(get_sch_field[0]);  //sch_date_from_を削除
        get_sch_field[1].parentNode.removeChild(get_sch_field[1]);  //sch_date_to_を削除
    }
}

//==================================================================
//以下、グループ操作系
//==================================================================
/**グループ編集 on */
function f_group_control_mode_on(mydocument){
    mydocument.getElementsByName("group_control_mode_on")[0].hidden = true;
    mydocument.getElementsByName("group_control_mode_off")[0].hidden = false;

    f_group_add_mode_on(mydocument);
    f_group_edit_mode_on(mydocument);
}
/**グループ編集 off */
function f_group_control_mode_off(mydocument){
    mydocument.getElementsByName("group_control_mode_on")[0].hidden = false;
    mydocument.getElementsByName("group_control_mode_off")[0].hidden = true;

    f_group_add_mode_off(mydocument);
    f_group_edit_mode_off(mydocument);
}


/**各フォームをグループとして結合するためのチェックボックスを追加する。*/
function f_group_add_mode_on(mydocument){
    //各フィールドのdivタグを取得。    
    let get_div = mydocument.getElementsByClassName("cls_grp_elem");

    //各フィールドのdivタグの子要素（先頭）にチェックボックスを追加
    let chk_box_add = new Array(get_div.length);
    for(let i = get_div.length - 1; i >= 0; i--){
        chk_box_add[i] = document.createElement('input'); 
        chk_box_add[i].type = 'checkbox'; 
        chk_box_add[i].className='grp_select_chkbox';
        chk_box_add[i].setAttribute('onclick', 'f_group_check(document)');
        get_div[i].insertBefore(chk_box_add[i], get_div[i].firstChild);
    }

    //コントロール系のボタンの表示／非表示と、有効／無効を調整
    mydocument.getElementsByName("group_add_and")[0].hidden = false;
    mydocument.getElementsByName("group_add_or")[0].hidden = false;
    for(let get_cls of mydocument.getElementsByClassName("cls_button_control1")){
        get_cls.disabled = "disabled";
    }
}

/**各フォームをグループとして結合するためのチェックボックスを削除する。*/
function f_group_add_mode_off(mydocument){
    //チェックボックスを削除
    let get_chkboxes = mydocument.getElementsByClassName("grp_select_chkbox");
    for(let i = get_chkboxes.length - 1; i >= 0; i--){
        get_chkboxes[i].parentNode.removeChild(get_chkboxes[i]);
    }

    //コントロール系のボタンの表示／非表示と、有効／無効を調整
    mydocument.getElementsByName("group_add_and")[0].hidden = true;
    mydocument.getElementsByName("group_add_and")[0].disabled = "disabled";
    mydocument.getElementsByName("group_add_or")[0].hidden = true;
    mydocument.getElementsByName("group_add_or")[0].disabled = "disabled";
    for(let get_cls of mydocument.getElementsByClassName("cls_button_control1")){
        get_cls.disabled = "";
    }
}

/**グループモードでチェックされている数≧2の場合、他のチェックボックスは選択不可にする。
 * また、グループモードonボタンを押下可能にする。
 * それ以外の場合、逆の操作を行う。
 */
function f_group_check(mydocument){
    
    let get_chkboxes = mydocument.getElementsByClassName("grp_select_chkbox");
    let grp_chkbox_count =0;
    //チェックされている数を確認
    for (let get_chkbox of get_chkboxes){if(get_chkbox.checked){grp_chkbox_count++}}
    
    //2以上はその他を選択不可に、2未満は全て選択可能にする。
    if(grp_chkbox_count >= 2){
        for (let get_chkbox of get_chkboxes){
            if(get_chkbox.checked){continue}else{get_chkbox.disabled="disabled";}
        }
        mydocument.getElementsByName("group_add_and")[0].disabled = "";
        mydocument.getElementsByName("group_add_or")[0].disabled = "";
    }else{
        for (let get_chkbox of get_chkboxes){get_chkbox.disabled="";}
        mydocument.getElementsByName("group_add_and")[0].disabled = "disabled";
        mydocument.getElementsByName("group_add_or")[0].disabled = "disabled";
    }
}

/**選択されたチェックボックスの間の要素をグループ化する*/
function f_group_add(mydocument,conjunction){
    //グループ化する要素を取得する。
    let get_grp_elem = mydocument.getElementsByClassName("cls_grp_elem");   //divタグ
    
    /*グループ化可能な要素より、チェックボックスが選択されている範囲を調査する。
      S：チェックボックスが選択されているスタートを調査中。
      E：チェックボックスが選択されているエンドを調査中。
    */
    let i_mode = 'S';
    let pos = new Object(); //連想配列を作成
    for(let i = 0; i < get_grp_elem.length ; i++){
        if(get_grp_elem[i].firstElementChild.checked){
            if(i_mode == 'S'){
                pos["start"] = i;
                i_mode = 'E';
            }else if(i_mode == 'E'){
                pos["end"] = i;
            }
        }
    }
    //グループカウントアップ ※グローバル変数
    grp_count++
    //グループ用のfieldsetタグを作成
    let grp_tag = document.createElement('fieldset'); 
    grp_tag.className ='cls_group '+ 'cls_group_'+conjunction;  //conjunctionにはandかorが入っている。
    grp_tag.name = 'group_'+grp_count;
    //grp_tag.innerHTML ='<legend>グループ'+grp_count+' ('+conjunction+'結合)'+'</legend>';

    //グループタグを、選択されている最後のdivタグの下に追加
    get_grp_elem[pos["end"]].parentNode.insertBefore(grp_tag, get_grp_elem[pos["end"]].nextSibling);
    //グループタグに対象の要素を移動。対象を下から順に移動していく。移動先は先頭の子要素とする。
    for(i = pos["end"]; i >= pos["start"] ; i--){
        grp_tag.insertBefore(get_grp_elem[i], grp_tag.firstChild);
    }
    //最後にグループタグ(fieldset)とセットのlegendタグを先頭の子要素に追加
    let legend_tag = document.createElement('legend'); 
    legend_tag.innerHTML = 'グループ'+grp_count+' ('+conjunction+'結合)'
    grp_tag.insertBefore(legend_tag, grp_tag.firstChild);

    //全てのチェックボックスを、非選択＆選択可能にする（初期状態）。
    let get_chkboxes = mydocument.getElementsByName("grp_select");
    for (let get_chkbox of get_chkboxes){
        get_chkbox.checked = false;
        get_chkbox.disabled = "";
    }
    //グループ追加and/or ボタンを選択不可にする（初期状態）。
    mydocument.getElementsByName("group_add_and")[0].disabled = "disabled";
    mydocument.getElementsByName("group_add_or")[0].disabled = "disabled";

    //追加後に、グループのリストを最新化。グループ追加／編集モードのon/offの機能で代用。
    f_group_add_mode_off(mydocument);
    f_group_add_mode_on(mydocument);
    f_group_edit_mode_off(mydocument);
    f_group_edit_mode_on(mydocument);
}

/**グループの削除のためのリストをチェックボックスで作る。
 */
function f_group_edit_mode_on(mydocument){

    //グループの数の確認と、グループのリストを作成。
    let get_grp_elem = mydocument.getElementsByClassName("cls_group");
    let get_control = mydocument.getElementsByName("controller_form");
    //グループ数の配列とインデックスを作成
    let edit_label = new Array(get_grp_elem.length);
    let edit_chg = new Array(get_grp_elem.length);
    let edit_del = new Array(get_grp_elem.length);
    //全グループを取得する。
    for (let i = 0; i <= get_grp_elem.length-1; i++ ){
        let legend_name = get_grp_elem[i].firstElementChild.innerHTML;  //グループの名前（「グループ2 (and結合)」のような値）を持って来る。
        let grp_name = get_grp_elem[i].name;  //グループの名前（group_2 のような値）を持って来る。

        //labelエレメントの中にチェックボックスを追加する。
        //また、追加したチェックボックスの右にグループの名称を表示させる。
        let l = "group_".length;  
        edit_label[i] = document.createElement("label"); 
        edit_label[i].className = "cls_edit_elem"
        edit_label[i].innerHTML = "<br>"+legend_name.split('(')[0]; //「グループ2 (and結合)」の間の(以降を除外して設定
        //and/orの切り替えボタンを作成
        edit_chg[i] = document.createElement('input'); 
        edit_chg[i].type = 'button';
        edit_chg[i].className = 'cls_edit_elem cls_edit_button';
        edit_chg[i].name = 'edit_button_change' + grp_name.substring(l,);
        edit_chg[i].value = 'and/or 反転';
        edit_chg[i].setAttribute('onclick', 'f_group_change(document,"'+ grp_name +'")');
        //削除ボタンを作成
        edit_del[i] = document.createElement('input'); 
        edit_del[i].type = 'button';
        edit_del[i].className = 'cls_edit_elem cls_edit_button';
        edit_del[i].name = 'edit_button_delete' + grp_name.substring(l,);
        edit_del[i].value = '削除';
        edit_del[i].setAttribute('onclick', 'f_group_delete(document,"'+ grp_name +'")');
        if(i==0){edit_del[i].disabled = "disabled";}     //グループ1だけは削除禁止

        //作成したlabelタグの子要素へ、チェンジボタンと削除ボタンを追加
        edit_label[i].appendChild(edit_chg[i]);
        edit_label[i].appendChild(edit_del[i]);
        //作成したlabelタグをコントロールエリアに追加
        get_control[0].appendChild(edit_label[i]);
    }
}

/**グループの削除のためのリストを消す。
 */
function f_group_edit_mode_off(mydocument){
    //削除対象となったグループを確認する。
    let get_grp_elem = mydocument.getElementsByClassName("cls_edit_elem");

    //取得したエレメント（チェックボックス）を下から順に消す。
    for(let i = get_grp_elem.length - 1; i >= 0; i--){
        get_grp_elem[i].parentNode.removeChild(get_grp_elem[i]);
    }
}

/**第二引数で指定されたグループのand/orを切り換える。
 * 第二引数：対象グループ（<fieldset>）のnameを設定していることを前提とする。
 */
function f_group_change(mydocument,grp_name){
    //grp_name(group_2のような名前が入っている）に指定されたタグを取得
    let get_grp_elem = mydocument.getElementsByName(grp_name);
    //取得した最初の子要素を取得。
    let legend_tg = get_grp_elem[0].firstChild;
    //取得したタグのクラス名を取得。
    let cls_nm = get_grp_elem[0].className;
    //クラス名に_or、_andの有無を確認し、orならand、andならorへチェンジ
    if(cls_nm.indexOf('_or',0) >= 0){
        get_grp_elem[0].className = cls_nm.replace('_or','_and');
        legend_tg.innerHTML = legend_tg.innerHTML.replace('or','and');
    }else if(cls_nm.indexOf('_and',0) >= 0){
        get_grp_elem[0].className = cls_nm.replace('_and','_or');
        legend_tg.innerHTML = legend_tg.innerHTML.replace('and','or');
    }
}

/**第二引数で指定されたグループを削除する。
 * 第二引数：対象グループ（<fieldset>）のnameを設定していることを前提とする。
 */
function f_group_delete(mydocument,grp_name){
    //grp_name(group_2のような名前が入っている）に指定されたタグを取得。
    let get_grp_elem = mydocument.getElementsByName(grp_name);
    let elem_children = get_grp_elem[0].children;   //取得したグループの子要素を配列にして取得。
    let fragment = document.createDocumentFragment();   //フラグメントエリア（中間ワーク的なドキュメント）を作成

    //最後の子要素から順にフラグメントの先頭に追加。ただし、fieldsetのlegendタグは単に削除する。
    for(let i = elem_children.length -1 ; i >= 0 ; i--){
        if(elem_children[i].tagName=='LEGEND'){
            elem_children[i].parentNode.removeChild(elem_children[i]);
        }else{
            fragment.insertBefore(elem_children[i], fragment.firstChild);   
        }
    }
    
    //フラグメントを対象のグループ（fieldset）の前に追加する。
    get_grp_elem[0].parentNode.insertBefore(fragment,get_grp_elem[0]);
    //不要になったfieldsetを削除
    get_grp_elem[0].parentNode.removeChild(get_grp_elem[0]);

    //削除後に、グループのリストを最新化。グループモードのon/offの機能で代用。
    f_group_edit_mode_off(mydocument);
    f_group_edit_mode_on(mydocument);
}

/**渡されたグループ名を検索し、グループ内の要素を配列にして返す。
 * 返す配列には、要素がグループであればグループ名、検索条件であれば、そのクエリーを設定する。
 */
function f_group_analysis(mydocument,grp_name,grp_analysis){
    let get_grp_elem = mydocument.getElementsByName(grp_name); //引数より渡されたグループ名を検索。
    
    //グループのクラス名に、or,andのどちらがあるか確認。        
    let cls_nm = get_grp_elem[0].className;
    let conjunction;    //現在分析中のグループのand/orの接続詞を保存するエリア。
    if(cls_nm.indexOf('_or',0) >= 0){
        conjunction = ' OR ';
    }else if(cls_nm.indexOf('_and',0) >= 0){
        conjunction = ' AND ';
    }
    let q_op_value;     //selectタグのoptionで選択されているvalueを保存するワーク。
    
    grp_analysis.push('(');                 //リストの先頭にグループの括弧を追加。
    for (let elem of get_grp_elem[0].children){     //fieldsetの子要素（孫は含まない）を順に処理する。
        if(elem.tagName == 'DIV'){
            for (let div_child_elem of elem.children){
                if(div_child_elem.tagName == 'SELECT'){
                    q_op_value = div_child_elem.value;
                }else if(div_child_elem.tagName == 'INPUT' && div_child_elem.type == 'text'){
                    if(q_op_value == 0){
                        grp_analysis.push('((title:'+div_child_elem.value+') OR article:('+div_child_elem.value+'))');
                    }else if(q_op_value == 1){
                        grp_analysis.push('title:('+div_child_elem.value+')');
                    }else if(q_op_value == 2){
                        grp_analysis.push('article:('+div_child_elem.value+')');
                    }else if(q_op_value == 4){
                        grp_analysis.push('issuer:('+div_child_elem.value+')');
                    }
               
                    grp_analysis.push(conjunction); //最後に接続詞（and/or）を追加。

                }else if(div_child_elem.tagName == 'INPUT' && div_child_elem.type == 'date'){
                    //publish_date :[2019-01-01T00:00:00Z TO 2019-01-31T23:59:59Z] 範囲指定の仕方
                    var wk_sch_date_from;
                    var wk_sch_date_to;
                    if(q_op_value == 3 && div_child_elem.name.substring(0,13) == "sch_date_from"){
                        //grp_analysis.push('(');
                        //grp_analysis.push('publish_date:'+div_child_elem.value);
                        if(div_child_elem.value == ""){
                            wk_sch_date_from = "1990-1-1";
                        }else{
                            wk_sch_date_from = div_child_elem.value;
                        }
                        //grp_analysis.push(' AND '); //最後に接続詞（and/or）を追加。
                    }else{
                        if(div_child_elem.value == ""){
                            wk_sch_date_to = now.getFullYear()+"-"+(now.getMonth()+1)+"-"+now.getDate()
                        }else{
                            wk_sch_date_to = div_child_elem.value;
                        }
                        grp_analysis.push("publish_date:["+wk_sch_date_from+"T00:00:00Z TO "+wk_sch_date_to+"T23:59:59Z]");
                        //grp_analysis.push(')');

                        grp_analysis.push(conjunction); //最後に接続詞（and/or）を追加。
                    }
                }
                /*
                }else if(div_child_elem.tagName == 'INPUT' && div_child_elem.type == 'checkbox' && div_child_elem.value == 'not_search'){
                    console.log('a3 '+div_child_elem.tagName+' '+div_child_elem.type+''+div_child_elem.value);
                }else{
                    console.log('a4 '+div_child_elem.tagName+' '+div_child_elem.type);
                }
                */
            }
        }else if(elem.tagName == 'FIELDSET'){
            grp_analysis.push([elem.name],conjunction);
        }
    }
    grp_analysis.pop();         //末尾に追加された余計なand/orを削除。
    grp_analysis.push(')');     //リストの末尾にグループの閉じ括弧を追加。
}
/**条件フィールドとグループを精査し、リクエストとしてサーバーに送る。
 * また、検索結果を表示するwindowを表示する。
 */
function f_search_results_window(mydocument){

    //クエリーを生成するための配列を宣言
    let solr_query_list = [['group_1']];
    let grp_check_flg = true;
    let grp_check = 'tmp';  //チェック中のグループを格納。対象が無くなった場合、''とする。

    let grp_analysis = [];

    //グループ1の要素から解析。
    let x = 0;  //無限ループ回避用。
    while(grp_check_flg){
        //solr_query_listを順に検査し、group_*の有無をチェックする。
        grp_check_flg = false;
        for(let i = 0; i < solr_query_list.length ;i++){
            if(toString.call(solr_query_list[i]) == '[object Array]'){
                grp_check_flg = true;   //type=リストが発見があった場合ture
                grp_analysis = [];      //結果の格納エリアを初期化
                f_group_analysis(mydocument,solr_query_list[i][0],grp_analysis);
                solr_query_list.splice(i,1);
                Array.prototype.splice.apply(solr_query_list,[i,0].concat(grp_analysis));
            }
        }
        x++
        if(x>=10){
            break;
        }
    }

    let elem = mydocument.getElementsByClassName("page_max_lines");
    let page_max_lines = elem[0].value;

    //window.open(window.location.origin+
    //    '/saikutu/kaisyuu/?sch_query='+solr_query_list.join('')+'&'+'page_num=1&page_max_lines='+page_max_lines+'&next_window=new');
    window.open(window.location.origin+
        '/saikutu/?sch_query='+solr_query_list.join('')+'&'+'page_num=1&page_max_lines='+page_max_lines+'&next_window=new');
    
}

/**ajax：条件フィールドとグループを精査し、リクエストとしてサーバーに送る。
 * また、検索結果を同じwindowのフレームに表示する。
 */
function f_search_results_frame(mydocument,page_num){
    //クエリーを生成するための配列を宣言
    let solr_query_list = [['group_1']];
    let grp_check_flg = true;
    let grp_check = 'tmp';  //チェック中のグループを格納。対象が無くなった場合、''とする。

    let grp_analysis = [];

    //グループ1の要素から解析。
    let x = 0;  //無限ループ回避用。
    while(grp_check_flg){
        //solr_query_listを順に検査し、group_*の有無をチェックする。
        grp_check_flg = false;
        for(let i = 0; i < solr_query_list.length ;i++){
            if(toString.call(solr_query_list[i]) == '[object Array]'){
                grp_check_flg = true;   //type=リストが発見があった場合ture
                grp_analysis = [];      //結果の格納エリアを初期化
                f_group_analysis(mydocument,solr_query_list[i][0],grp_analysis);
                solr_query_list.splice(i,1);
                Array.prototype.splice.apply(solr_query_list,[i,0].concat(grp_analysis));
            }
        }
        x++
        if(x>=10){
            break;
        }
    }
    
    let elem = mydocument.getElementsByClassName("page_max_lines");
    let page_max_lines = elem[0].value;

    //ajaxで検索条件をクエリーで送信する。
    xhr_request = new XMLHttpRequest();
    xhr_request.onreadystatechange = f_hxr_showData;
    xhr_request.open("GET",window.location.origin+
        '/saikutu/?sch_query='+solr_query_list.join('')+'&'+'page_num='+page_num+'&'+'page_max_lines='+page_max_lines+'&next_window=same',true);
    xhr_request.send(null);

    /**
    ajaxで取得したhtmlを、divタグ（name=hokanko）に挿入する。
     */
    function f_hxr_showData(){
        if (xhr_request.readyState == 4 && xhr_request.status == 200){
            let get_hokanko_elem = mydocument.getElementsByName("hokanko")[0];
            get_hokanko_elem.innerHTML = xhr_request.responseText;
        }
    }
}

/**ajax：ページボタンを押下された場合、初回検索時の検索条件を基に
 * 指定ページのリクエストとしてサーバーに送る。
 * また、検索結果を同じwindowのフレームに表示する。
 */
function f_page_move(mydocument,page_num){

    let sch_query = mydocument.getElementsByName("sch_query_save")[0].value;
    let page_max_lines = mydocument.getElementsByName("page_max_lines_save")[0].value;
    
    //ajaxで検索条件をクエリーで送信する。
    xhr_request = new XMLHttpRequest();
    xhr_request.onreadystatechange = f_hxr_showData;
    xhr_request.open("GET",window.location.origin+
        '/saikutu/?sch_query='+sch_query+'&'+'page_num='+page_num+'&'+'page_max_lines='+page_max_lines+'&next_window=same',true);
    xhr_request.send(null);

    /**
    ajaxで取得したhtmlを、divタグ（name=hokanko）に挿入する。
     */
    function f_hxr_showData(){
        if (xhr_request.readyState == 4 && xhr_request.status == 200){
            let get_hokanko_elem = mydocument.getElementsByName("hokanko")[0];
            get_hokanko_elem.innerHTML = xhr_request.responseText;
        }
    }
}