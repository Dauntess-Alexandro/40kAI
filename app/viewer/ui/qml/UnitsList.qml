import QtQuick 2.15
import QtQuick.Controls 2.15

ListView {
    id: unitsList
    clip: true
    spacing: 4
    model: viewerUnitsModel
    cacheBuffer: 400

    ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

    function scrollToUnitId(uid) {
        if (!viewerUnitsModel || uid < 0) return
        for (var i = 0; i < viewerUnitsModel.rowCount(); i++) {
            var row = viewerUnitsModel.rowAt(i)
            if (row.unitId !== uid) continue
            var item = unitsList.itemAtIndex(i)
            var needsScroll = item === null
            if (!needsScroll && item) {
                var top = unitsList.contentY
                var bottom = top + unitsList.height
                needsScroll = item.y < top || item.y + item.height > bottom
            }
            if (needsScroll)
                unitsList.positionViewAtIndex(i, ListView.Center)
            break
        }
    }

    delegate: UnitCard {
        width: unitsList.width
        readonly property var row: viewerUnitsModel ? viewerUnitsModel.rowAt(index) : ({})
        unitId: row.unitId !== undefined ? row.unitId : -1
        unitSide: row.unitSide !== undefined ? row.unitSide : ""
        unitName: row.unitName !== undefined ? row.unitName : "—"
        unitHp: row.unitHp !== undefined ? row.unitHp : "—"
        unitModels: row.unitModels !== undefined ? row.unitModels : "—"
        unitIconPath: row.unitIconPath !== undefined ? row.unitIconPath : ""
        unitFactionLabel: row.unitFactionLabel !== undefined ? row.unitFactionLabel : ""
        unitIsActive: row.unitIsActive === true
        unitIsSelected: row.unitIsSelected === true
        unitIsDamaged: row.unitIsDamaged === true
        unitSection: row.unitSection !== undefined ? row.unitSection : ""
    }

    Label {
        anchors.centerIn: parent
        visible: !viewerUnitsModel || viewerUnitsModel.rowCount() === 0
        text: qsTr("Нет отрядов на поле.\nЗапустите матч из меню «Игра».")
        color: textSecondaryColor
        font.pixelSize: fontMd
        wrapMode: Text.Wrap
        horizontalAlignment: Text.AlignHCenter
        width: unitsList.width - 20
    }

    Connections {
        target: viewerController
        enabled: viewerController !== null && viewerController !== undefined
        function onUnitsScrollTargetIdChanged() {
            if (!viewerController) return
            var uid = viewerController.unitsScrollTargetId
            if (uid < 0) return
            unitsList.scrollToUnitId(uid)
        }
        function onSelectedUnitIdChanged() {
            Qt.callLater(function () {
                if (!viewerController || viewerController.selectedUnitId < 0) return
                unitsList.scrollToUnitId(viewerController.selectedUnitId)
            })
        }
    }
}
