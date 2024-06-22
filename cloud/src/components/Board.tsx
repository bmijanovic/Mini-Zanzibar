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
import 'tldraw/tldraw.css'
import _jsonSnapshot from '../temp.json'
import * as fs from "fs";
import {useNavigate, useParams} from "react-router-dom";

// There's a guide at the bottom of this file!

const jsonSnapshot = _jsonSnapshot as any as TLEditorSnapshot


export default function Board() {
    const { id } = useParams();

    function CustomMainMenu() {

        const editor=useEditor();
        return (
            <DefaultMainMenu>
                <div style={{ backgroundColor: 'thistle' }}>
                    <TldrawUiMenuGroup id="example">
                        <TldrawUiMenuItem
                            id="save"
                            label="Save"
                            icon="external-link"
                            readonlyOk
                            onSelect={() => {
                                const { document, session } = getSnapshot(editor.store)
                                const jsonString = JSON.stringify({document,session});

                                const filePath = '../temp.json';


                            }}
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
        <div style={{ position: 'fixed', inset: 0 }} className="tldraw__editor">
            <Tldraw
                onMount={(editor) => {
                    editor.updateInstanceState({ isReadonly: false })
                }}
                snapshot={jsonSnapshot}
                components={components}
            />

        </div>
    )
}