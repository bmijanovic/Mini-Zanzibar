import {
    TLEditorSnapshot,
    Tldraw,
    useEditor,
    DefaultMainMenu,
    TldrawUiMenuGroup,
    TldrawUiMenuItem,
    getSnapshot,
    TLComponents,
    ExportFileContentSubMenu,
    ViewSubmenu
} from 'tldraw'
import 'tldraw/tldraw.css';
import {useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";


export default function Board() {
    const {id} = useParams();
    const [board, setBoard] = useState(null);
    const [isReadOnly, setIsReadOnly] = useState(true);

    useEffect(() => {
        axios.get(`http://localhost:8001/boards/${id}`)
            .then(res => {
                res = res.data;
                console.log(res)
                setIsReadOnly(res.privilege === 'viewer')
                setBoard(res);
            })
    }, [])

    const saveBoard = (editor) => {
        const {document, session} = getSnapshot(editor.store)
        const jsonString = JSON.stringify({document, session});

        axios.put(`http://localhost:8001/boards`, {board_content: jsonString, board_id: id})
            .then(res => {
            })
    }

    function CustomMainMenu() {

        const editor = useEditor();
        return (
            <DefaultMainMenu>
                <div style={{backgroundColor: 'thistle'}}>
                    <TldrawUiMenuGroup id="example">
                        <TldrawUiMenuItem
                            id="save"
                            label="Save"
                            icon="external-link"
                            readonlyOk
                            onSelect={() => saveBoard(editor)}
                        />
                        <ExportFileContentSubMenu/>
                        <ViewSubmenu/>
                    </TldrawUiMenuGroup>
                </div>
            </DefaultMainMenu>
        )
    }

    const components: TLComponents = {
        MainMenu: CustomMainMenu,
    }
    return (
        <div style={{position: 'fixed', inset: 0}} className="tldraw__editor">
            {board != null &&
                <Tldraw
                    onMount={(editor) => {
                        editor.updateInstanceState({isReadonly: isReadOnly})
                    }}
                    snapshot={board.content as any as TLEditorSnapshot}
                    components={components}
                />}

        </div>
    )
}